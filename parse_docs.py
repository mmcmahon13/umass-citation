import xml.etree.ElementTree as ET

def citation_dfs(root, label_string, write_file):
    for elem in root:
        if len(elem) == 0:
            # split text into individual words
            words = elem.text.split(' ')
            # assign BILOU tags and write to output file
            for word in words:
                if word.strip() != '':
                    # write in a few dummy values because the preprocessing code expects them
                    if(label_string != '/' or elem.tag != None):
                        write_file.write((word + ' d d ' + label_string + '/' + elem.tag + '\n').encode('utf8'))
                    else:
                        print "word has no label"
                        write_file.write((word + ' d d O\n').encode('utf8'))
            # print elem.text, label_string + '/' + elem.tag
        else:
            citation_dfs(elem, label_string + '/' + elem.tag, write_file)

def parse_file(filename):
    with open(filename, 'rb') as dev_file:
        num_dev = 0
        with open(filename + '.parsed', 'wb') as parsed_dev_file:
            for citation in dev_file:
                num_dev += 1
                citation = "<citation> " + citation + " </citation>"
                citation = citation.replace('&', '&amp;')
                try:
                    root = ET.fromstring(citation)
                    citation_dfs(root, '', parsed_dev_file)
                    parsed_dev_file.write('\n')
                except ET.ParseError:
                    print citation
            parsed_dev_file.flush()
            parsed_dev_file.close()
        print num_dev
        dev_file.close()

parse_file('dev.docs')
parse_file('testing.docs')
parse_file('training.docs')





