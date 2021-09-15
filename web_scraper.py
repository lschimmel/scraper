from bs4 import BeautifulSoup
import requests
import os
import pathlib
import re
import csv
N = 100

# scrapes webpage's search results
# saves a subset of the webpage, and images to a folder


def main():
    #test conditions
    # url = 'URL GOES HERE'
    # i = 1
    # scrape_how_to(url, i)
    # log = ['test', 'item']
    # failed = ['fone', 'f2']
    # i = 0
    # savelog(failed, log, i)


    # run conditions
    log = []
    failed = []
    for i in range(0, N):
        if i == (N/2):
            savelog(log, failed, i)
        else:
            print('\npage: ', i, '\n____________________________________________________________________________________')
            try:
                filename = search_results(i, failed)
                url = next_url(filename, i, log)
            except Exception:
                pass
    print('failed:\n', failed)
    savelog(log, failed, i)

def savelog(log, failed, i):
    filename = 'log' + str(i) + '.txt'
    filename_csv = 'log' + str(i) + '.csv'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('log\n')
        for item in log:
            f.write(str(item))
            f.write('\n')
        f.write('\n\nfailed\n')
        for item in failed:
            f.write(str(item))
            f.write('\n')

    with open(filename_csv, 'w') as e:
        writer = csv.writer(e)
        for item in log:
            writer.writerow([item])



def scrape_search_results(i, failed):
    url = 'URL GOES HERE' + str(i*24)
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    # print(soup)
    soupa = soup.find_all('a')
    filename = 'searchresults' + str(i) + '.txt'
    link_set = set()
    for link in soupa:
        link_txt = str(link.get('href')) + "\n"
        link_set.add(link_txt)
    # print('link set:', link_set)
    with open(filename, 'w') as f:
        for item in link_set:
            # print(item)
            link_txt1 = str(item)
            link_txt2 = link_txt1.replace('\\', '')
            link_txt3 = link_txt2.replace('"n', '')
            link_txt4 = link_txt3.replace('"', '')
            # print('link text 4:', link_txt4)
            if 'URL GOES HERE' in link_txt4:
                if not "specialoffers" in link_txt4 and not "sale" in link_txt4:
                   f.write(link_txt4)
            else:
                failed.append(link_txt4)
    return filename

def next_url(filename, i, log):
    #iterates over each url in a .txt file, scrapes the webpage for instructions and saves the result in a txt file (file name is the url, first element is the url, second element is either the instructions or the full scrape
    with open(filename, 'r') as f:
        for row in f:
            url = str(row)
            # print(url)
            scrape_how_to(url, i, log)
    # return url

def scrape_how_to(urlstringname, i, log):
    #test conditions
    url = urlstringname.strip('\n')
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "lxml")
    soup_content = soup.find_all('div', attrs={'class':'loc content-body'})
    #find subsections of the soup
    #breadcrumbs for subfolders
    breadcrumbs = soup.find('div', attrs= {'class': 'breadcrumbs'})
    i = 0
    pathlevel0 = 'output_dir'
    if breadcrumbs:
        for child in breadcrumbs:
            if child.string != '\n' and child.string != None:
                if i == 0:
                    i += 1
                    # print(i, child.string)
                    foldername = 'lvl' + str(i) + '_' + child.string
                    pathlevel1 = pathlib.Path(pathlevel0, foldername)
                    if pathlevel1.exists():
                        # print('folder level', i, 'exists')
                        pathlevelj = pathlevel1
                        pass
                    else:
                        pathlevel1.mkdir(parents=True, exist_ok=False)
                    pathlevelk = pathlib.Path(pathlevel1)
                    # pathlevelj = pathlib.Path(pathlevelk, foldername)
                else:
                    i += 1
                    foldername = 'lvl' + str(i) + '_' + child.string
                    pathlevelj= pathlib.Path(pathlevelk, foldername)
                    if pathlevelj.exists():
                        # print('folder level', i, 'exists')
                        pathlevelk = pathlib.Path(pathlevelj)
                    else:
                        # print('creating new level 1 folder: ', child.string)
                        pathlevelj.mkdir(parents=True, exist_ok=False)
                        pathlevelk = pathlib.Path(pathlevelj)
    else:
        pathlevelj = pathlib.Path(pathlevel0, 'Uncategorized')

    #body content

    soupa = soup.find_all('div', attrs={'class': 'loc content'})
    url_name = url.replace('https://', '-')
    url_name2 = url_name.replace('/', '-')
    #make folders and name them + files according to headers
    try:
        valid_file_name = re.sub('[^\w_.)( -]', '', soup.h1.string)
    except Exception:
        try:
            valid_file_name = re.sub('[^\w_.)( -]', '', soup.h2.string)
        except Exception:
            valid_file_name = 'scrapedarticle_' + str(i) + '.txt'
    foldername = valid_file_name.strip(' ')
    new_dir_name = 'a_' + foldername

    if i == 1:
        project_dir_name = pathlib.Path(pathlevel1, new_dir_name)
    else:
        project_dir_name = pathlib.Path(pathlevelj, new_dir_name)
    new_dir = pathlib.Path(project_dir_name)
    new_dir.mkdir(parents=True, exist_ok=True)

    img_tags = soup.find_all('img')
    try:
    # save image urls as txt files
        urls = [img['data-src'] for img in img_tags]
        i = 0
        for url in urls:
            i += 1
            image_filename = 'image_' + str(i) + '.txt'
            with open(project_dir_name/image_filename, 'w') as f:
                f.write(url)
    except Exception:
        image_filename = 'image_' + str(i) + '.txt'
        # print(url)
        with open(project_dir_name / image_filename, 'w', encoding='utf-8') as f:
            f.write(str(urlstringname))
            f.write('\nerror, saved img_tags instead\n')
            f.write(str(img_tags))
        pass

    # checks if there is an article container content section, else if there is an instruction section class, else returns full soup
    # save contents as txt file
    filename = foldername + '.txt'
    log.append(filename)
    log.append(urlstringname)
    try:
        if soup_content:
            with open(new_dir/filename, 'w', encoding="utf-8") as f:
                f.write(str(urlstringname))
                f.write(str(soup_content))
        elif soupa:
            with open(new_dir/filename, 'w', encoding="utf-8") as f:
                f.write(str(urlstringname))
                f.write('\naloc content-body not found, pulled loc content instead. \n\n')
                f.write(str(soupa))
        else:
            with open(new_dir/filename, 'w', encoding="utf-8") as f:
                f.write(str(urlstringname))
                f.write('\nloc content-body not found, pulled soup instead. \n\n')
                f.write(str(soup))
    except Exception:
        pass
    # print(log)
    return log


if __name__ == "__main__":
    main()

