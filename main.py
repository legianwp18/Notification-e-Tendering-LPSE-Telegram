from warnings import catch_warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil, os, requests
from datetime import datetime
import json

list_web = "list_web.txt"
key_list = 'key_list.txt'
tender_list = 'tender_list.txt'
nontender_list = 'nontender_list.txt'
LOGFILE = "etender_log.txt"

path = dest_dir = os.path.abspath(os.getcwd())
source_tander = path+"/"+tender_list
source_nontander = path+"/"+nontender_list
destination_tander = path+"/"+tender_list.replace(".txt","")+"_backup.txt"
destination_nontander = path+"/"+nontender_list.replace(".txt","")+"_backup.txt"

#MENYIMPAN LOG APLIKASI
def writeLog (logString):
	print(logString)
	with open(LOGFILE, 'a') as f:
		f.write(('%s - %s\n' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), logString)))
	f.close()

def telbot_sendtext(bot_message, bot_chatID = '-1001388736895'):
    bot_token = '1576122078:AAFCjeZCycHv0_DpEjxu6d_Qwqmkhct5zNQ'
    sent_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(sent_text)
    return response.json()

key = []
for k in open(key_list, 'r') :
    key.append(k.replace("\n",""))

for web in open(list_web, "r"):
    try:
        website = web.replace("\n","")
        chrome_options = Options()
        chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(website)
        parent_han  = driver.window_handles
        title = driver.title
        print(title)
        # TENDER
        try:
            sum_barang = int(driver.find_element_by_xpath('//*[@class="content"]/div[2]/div/div/table/tbody/tr/td/span').text)
            if sum_barang > 0:
                main = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "Pengadaan_Barang"))
                )
                tender_details = []
                for list in main:
                    with open(tender_list, 'r') as r:
                        tender = json.load(r)
                    r.close()
                    # print("Buka file")
                    # print(tender)
                    tender_details = tender
                    content = list.find_elements_by_tag_name("td")
                    kode = content[1].find_elements_by_tag_name("a")[0].get_attribute('href').split("/")[5]
                    name = content[1].find_elements_by_tag_name("a")[0].text
                    hps = content[2].text
                    last_reg = content[3].text
                    url = content[1].find_elements_by_tag_name("a")[0].get_attribute('href')

                    for k in key :
                        if k in name:
                            if kode not in tender:
                                print("||=====================================================||")
                                print('Judul : %s' % title)
                                print('No : %s' % content[0].text)
                                print('Kode Tender : %s' % kode)
                                print('Nama Paket : %s' % name)
                                print('HPS : %s' % hps)
                                print('Akhir Pendaftarab : %s' % last_reg)
                                print('Url Website : %s' % website)
                                print('Url Detail : %s' % url)

                                message = '*New Tander*\n%s\n\n-Kode Tender : %s\n-Nama Paket : %s\n-HPS : %s\n-Akhir Pendaftaran : %s\n %s' % (title,kode,name,hps,last_reg,url)
                                response = telbot_sendtext(bot_message=message,bot_chatID='-1001388736895')
                                print(response)

                                tender_details.append(kode)
                                # print("Apend kode")
                                # print(tender_details)
                                break

                    # list.find_element_by_link_text(content[1].find_elements_by_tag_name("a")[0].text).click()
                    
                    # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    # all_han = driver.window_handles
                    # driver.switch_to.window(all_han[1])
                    # main2 = driver.find_elements_by_class_name("content")
                    # for isi in main2:
                    #     print("=====================================================")
                    #     print("======PENGUMUMAN======")
                    #     print('Kode Tender : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr/td').text)
                    #     print('Nama Tender : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[2]/td').text)
                    #     print('Kode RUP : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td').text)
                    #     print('Nama Paket : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]').text)
                    #     print('Sumber Dana : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[3]').text)
                    #     print('Tanggal Pembuatan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[4]/td').text)
                    #     print('Keterangan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[5]/td').text)
                    #     print('Tahap Tender Saat ini : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[6]/td').text)
                    #     print('Instansi : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[7]/td').text)
                    #     print('Satuan Kerja : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[8]/td').text)
                    #     print('Kategori: %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[9]/td').text)
                    #     print('Sistem Pengadaan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[10]/td').text)
                    #     print('Tahun Anggaran : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[11]/td').text)
                    #     print('Nilai Pagu Paket : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[12]/td').text)
                    #     print('Nilai HPS Paket : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[12]/td[2]').text)
                    #     print('Cara Pembayaran : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[13]/td').text)
                    #     print('Lokasi Pekerjaan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[14]/td').text)
                    #     print('Kualifikasi Usaha : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[15]/td').text)
                    #     print('Peserta Tender : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[17]/td').text)
                    #     print("=====================================================")
                    # driver.close()
                    # time.sleep(1)
                    # driver.switch_to.window(all_han[0])
                    # break  
                    # print("simpan")
                    # print(tender_details)
                    if tender_details:
                        with open(tender_list, 'w') as w:
                            json.dump(tender_details, w)
                        w.close()
                        dest = shutil.copyfile(source_tander, destination_tander)
        except Exception as e:
            writeLog(title)
            writeLog(e)
        # PENGADAAN LANGSUNG
        try:
            sum_barang = int(driver.find_element_by_xpath('//*[@class="content"]/div[2]/div/div[2]/table/tbody/tr/td/span').text)
            if sum_barang > 0:
                main = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "Pengadaan_Barang_pl"))
                )
                nontender_details = []
                for list in main:
                    with open(nontender_list, 'r') as r:
                        nontender = json.load(r)
                    r.close()
                    # print("Buka file")
                    # print(tender)
                    nontender_details = nontender
                    content = list.find_elements_by_tag_name("td")
                    kode = content[1].find_elements_by_tag_name("a")[0].get_attribute('href').split("/")[5]
                    name = content[1].find_elements_by_tag_name("a")[0].text
                    hps = content[2].text
                    last_reg = content[3].text
                    url = content[1].find_elements_by_tag_name("a")[0].get_attribute('href')

                    for k in key :
                        if k in name:
                            if kode not in nontender:
                                print("||=====================================================||")
                                print('Judul : %s' % title)
                                print('No : %s' % content[0].text)
                                print('Kode Tender : %s' % kode)
                                print('Nama Paket : %s' % name)
                                print('HPS : %s' % hps)
                                print('Akhir Pendaftaran : %s' % last_reg)
                                print('Url Website : %s' % website)
                                print('Url Detail : %s' % url)

                                message = '*New Penunjukan Langsung*\n%s\n\n-Code Tender : %s\n-Nama Paket : %s\n-HPS : %s\n-Akhir Pendaftaran : %s\n %s' % (title,kode,name,hps,last_reg,url)
                                response = telbot_sendtext(bot_message=message,bot_chatID='-1001388736895')
                                print(response)

                                nontender_details.append(kode)
                                # print("Apend kode")
                                # print(nontender_details)
                                break

                    # list.find_element_by_link_text(content[1].find_elements_by_tag_name("a")[0].text).click()
                    
                    # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    # all_han = driver.window_handles
                    # driver.switch_to.window(all_han[1])
                    # main2 = driver.find_elements_by_class_name("content")
                    # for isi in main2:
                    #     print("=====================================================")
                    #     print("======PENGUMUMAN======")
                    #     print('Kode Tender : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr/td').text)
                    #     print('Nama Tender : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[2]/td').text)
                    #     print('Tanggal Pembuatan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[3]/td').text)
                    #     print('Keterangan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[4]/td').text)
                    #     print('Tahap Tender Saat ini : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[5]/td').text)
                    #     print('Instansi : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[6]/td').text)
                    #     print('Satuan Kerja : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[7]/td').text)
                    #     print('Kategori: %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[8]/td').text)
                    #     print('Sistem Pengadaan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[9]/td').text)
                    #     print('Tahun Anggaran : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[10]/td').text)
                    #     print('Nilai Pagu Paket : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[11]/td').text)
                    #     print('Nilai HPS Paket : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[11]/td[2]').text)
                    #     print('Lokasi Pekerjaan : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[12]/td').text)
                    #     print('Kualifikasi Usaha : %s' % isi.find_element_by_xpath('//*[@class="content"]/table/tbody/tr[13]/td').text)
                    #     print("=====================================================")
                    # driver.close()
                    # time.sleep(1)
                    # driver.switch_to.window(all_han[0])
                    # break  
                    # print("simpan")
                    # print(nontender_details)
                    if nontender_details:
                        with open(nontender_list, 'w') as w:
                            json.dump(nontender_details, w)
                        w.close()
                        dest = shutil.copyfile(source_nontander, destination_nontander)
        except Exception as e:
            writeLog(title)
            writeLog(e)
    except Exception as e:
        writeLog(e)
    driver.quit()