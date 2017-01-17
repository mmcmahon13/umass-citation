import xml.etree.ElementTree as ET

def citation_dfs(root, label_string, write_file):
    prev_elem = ""
    for j,elem in enumerate(root):
        # if we're at a token/entity, write it to the file along with its label
        if len(elem) == 0:
            # split text into individual words
            words = elem.text.split(' ')
            filtered_words = [word for word in words if word.strip() != '']

            # assign BILOU tags and write to output file
            num_tokens = len(filtered_words)
            for i,word in enumerate(filtered_words):
                bilou_label = ""
                if num_tokens < 2:
                    bilou_label = "U-"
                else:
                    if i == 0:
                        bilou_label = "B-"
                    # elif i == num_tokens-1:
                    #     bilou_label = "L-"
                    else:
                        bilou_label = "I-"

                # write in a few dummy values because the preprocessing code expects them
                if(label_string != '/' or elem.tag != None):
                    write_file.write((word + ' d d ' + label_string + '/' + bilou_label + elem.tag + '\n').encode('utf8'))
                else:
                    print "word has no label"
                    write_file.write((word + ' d d O\n').encode('utf8'))
            # print elem.text, label_string + '/' + elem.tag
        else:
            bilou_label = ""
            # TODO: this isn't the correct BIO scheme, write another function to pass over the output and fix it?
            if len(root) < 2:
                bilou_label = "U-"
            else:
                if elem.tag != prev_elem:
                    bilou_label = "B-"
                else:
                    bilou_label = "I-"
            citation_dfs(elem, label_string + '/' + bilou_label + elem.tag, write_file)
        prev_elem = elem.tag

def fix_heirarchical_bio(citation_tokens):
    pass

def parse_file(filename):
    with open(filename, 'rb') as file:
        num_dev = 0
        with open(filename + '.parsed', 'wb') as parsed_file:
            for citation in file:
                num_dev += 1
                citation = "<citation> " + citation + " </citation>"
                citation = citation.replace('&', '&amp;')
                try:
                    root = ET.fromstring(citation)
                    citation_dfs(root, '', parsed_file)
                    parsed_file.write('\n')
                except ET.ParseError:
                    print citation
            parsed_file.flush()
            parsed_file.close()
        print num_dev
        file.close()

parse_file('dev.docs')
parse_file('testing.docs')
parse_file('training.docs')





