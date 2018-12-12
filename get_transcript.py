from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import io
import os
import traceback

selenium_chrome_path = 'selenium-3.14.1/chromedriver'
search_terms = "reducedlinks.txt"
first_search_index=0


class GoogleTestCase():
    
    def setUp(self):
        self.browser = webdriver.Chrome(selenium_chrome_path)

    def testPageTitle(self, url):
        self.browser.get(url)
        vidid = url.split("v=")[-1]
        if not os.path.isdir("youtube"):
            mkdir("youtube")
        if no os.path.isdir("youtube/transcripts")
            mkdir("youtube/transcripts")
        f = io.open("youtube/transcripts/"+vidid.replace('\n','') + ".txt","w",encoding='utf-8')
        try:
            dots = WebDriverWait(self.browser, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'[aria-label="More actions"]'))
            )
            dots.click()
            open_btn = WebDriverWait(self.browser,1).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'ytd-menu-service-item-renderer yt-formatted-string'))
            )
            open_btn.click()
            try:
                all_trans = WebDriverWait(self.browser,10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR,'ytd-transcript-renderer paper-button'))
                )
                all_trans.click() 
    
                open_transcripts = WebDriverWait(self.browser,1).until(
                                    EC.presence_of_element_located(
                                        (By.CSS_SELECTOR,'ytd-transcript-renderer a.yt-dropdown-menu')
                                    )
                )

                open_transcripts = self.browser.find_elements(By.CSS_SELECTOR,"ytd-transcript-renderer a.yt-dropdown-menu")

                title = WebDriverWait(self.browser,10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'h1.title yt-formatted-string'))
                    ).text

                owner = WebDriverWait(self.browser,10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'#owner-name a'))
                    ).text


                try:
                    subscribers = WebDriverWait(self.browser,2).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR,'#subscribe-button .deemphasize'))
                        ).text
                except:
                    subscribers="0"


                show_more = WebDriverWait(self.browser,2).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'#more'))
                    )
                show_more.click()
                
                description = WebDriverWait(self.browser,2).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'#description'))
                    ).text

                ActionChains(self.browser).move_to_element((By.CSS_SELECTOR,'ytd-metadata-row-container #collapsible'))

                metadata = WebDriverWait(self.browser,2).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'#collapsible'))
                    ).text
                

                try:
                    comments = WebDriverWait(self.browser,2).until(
                                       EC.presence_of_element_located((By.CSS_SELECTOR,'.count-text'))
                        ).text
                except:
                    comments="0"

                views = WebDriverWait(self.browser,2).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'.view-count'))
                    ).text
                try:
                    likes = WebDriverWait(self.browser,2).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR,'[aria-label$="likes"]'))
                        ).text
                except:
                    likes="0"
                try:
                    dislikes = WebDriverWait(self.browser,2).until(
                                        EC.presence_of_element_located((By.CSS_SELECTOR,'[aria-label$="dislikes"]'))
                        ).text
                except:
                    dislikes = "0"

                date = WebDriverWait(self.browser,2).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'.date'))
                    ).text
                f.write(unicode("<<~~ Metadata ~~>>\r"))
		f.write(unicode(title + "\r" + owner +"\r"+ subscribers +"\r"+ comments +"\r"+  views +"\r"+ likes +"\r"+ dislikes +"\r"+ date))
                f.write(unicode("\r<<~~ Description ~~>>\r" + description))
                f.write(unicode("\r<<~~ Category ~~>>\r" + metadata))
                if len(open_transcripts) > 1:
                  open_transcripts = open_transcripts[:-1]
            
                for trans_type in open_transcripts:
                    test1 = ActionChains(self.browser).move_to_element(all_trans).click(all_trans).perform()
                    not_done = True
                    i = 0
                    while not_done and i < 10 and len(open_transcripts) > 1:
                        i+=1
                        try:
                          WebDriverWait(self.browser, 1).until(EC.visibility_of(trans_type)).click()
                          not_done = False
                        except: 
                          ActionChains(self.browser).move_to_element(all_trans).click(all_trans).perform()
                    
                    WebDriverWait(self.browser,2)
                    
                    transcript = WebDriverWait(self.browser,2).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR,'ytd-transcript-body-renderer'))
                    )
                    text = transcript.text
                    f.write(unicode("\r<<~~ Transcript ~~>>\r"))
                    f.write(unicode(text))
            except Exception as e:
                print(traceback.format_exc())
                transcript = WebDriverWait(self.browser,1).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR,'ytd-transcript-body-renderer'))
                )
                text = transcript.text
                f.write(unicode("\r<<~~ Transcript ~~>>\r"))
                f.write(unicode(text))                
        except Exception as e:
            print(traceback.format_exc())
            pass

        finally:
            f.close()
            self.browser.quit()
            pass


if __name__ == '__main__':
  f = io.open(search_terms,"r",encoding="utf-8")
  links = f.readlines()
  i=0
  for link in links:
    i+=1
    if i > first_search_index:
      print(i)
      try:
        driver = GoogleTestCase()
        driver.setUp()
        driver.testPageTitle(link)
      except Exception as e:
        print(traceback.format_exc()) 
