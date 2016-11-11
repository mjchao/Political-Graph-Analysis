from bs4 import BeautifulSoup
import urllib2

cid = []
cycle = []

outfile = open('contributions.csv', 'w')

formatURL = 'http://opensecrets.org/politicians/contrib.php?cid=%s&cycle=%s&type=I&newMem=N&recs=100'
hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }

counter = 0

with open('ids.csv', 'r') as f:

  for line in f:
    # Test for one politican
    # if counter > 0:
    #   break;
    # counter = counter + 1

    # Form URL
    line = line[:-1]
    param = line.split(',')  
    url = formatURL % (param[0], param[1])

    # Form request
    req = urllib2.Request(url, headers=hdr)

    # Make URL request
    try:
      page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
      print e.fp.read()

    # Retrieve request
    content = page.read()
    # print content

    # Get table content
    soup = BeautifulSoup(content, "lxml")
    table = soup.find("table", attrs={"id":"topContrib"})

    # The first tr contains the field names.
    # headings = [th.get_text() for th in table.find("tr").find_all("th")]
    # print headings

    # Parse rows of table and print to CSV outfile
    for row in table.find_all("tr")[1:]:
      # dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
      dataCol = param + [td.get_text() for td in row.find_all("td")]
      dataStr = ','.join(dataCol)
      outfile.write(dataStr.encode('utf8') + '\n')
    print param[0], param[1]

outfile.close()
