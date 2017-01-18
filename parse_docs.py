import xml.etree.ElementTree as ET

# def citation_dfs(root, label_string, write_file):
def citation_dfs(root, label_string, token_dict):
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
                # if num_tokens < 2:
                #     bilou_label = "U-"
                # else:
                #     if i == 0:
                #         bilou_label = "B-"
                #     # elif i == num_tokens-1:
                #     #     bilou_label = "L-"
                #     else:
                #         bilou_label = "I-"

                # write in a few dummy values because the preprocessing code expects them
                # if(label_string != '/' or elem.tag != None):
                #     write_file.write((word + ' d d ' + label_string + '/' + bilou_label + elem.tag + '\n').encode('utf8'))
                # else:
                #     print "word has no label"
                #     write_file.write((word + ' d d O\n').encode('utf8'))

                # token_dict is actually a list of tuples, so that the words will be in order
                # token_dict.append((word, label_string.split("/")[1:] + [bilou_label + elem.tag]))
                token_dict.append((word, label_string.split("/")[1:] + ["0-" + elem.tag]))

            # print elem.text, label_string + '/' + elem.tag
        else:
            bilou_label = ""
            # TODO: this isn't the correct BIO scheme, write another function to pass over the output and fix it?
            # if len(root) < 2:
            #     bilou_label = "U-"
            # else:
            #     if elem.tag != prev_elem:
            #         bilou_label = "B-"
            #     else:
            #         bilou_label = "I-"

            # separate the different things somehow?
            # citation_dfs(elem, label_string + '/' + str(j) + "-" + elem.tag, write_file)
            citation_dfs(elem, label_string + '/' + str(j) + "-" + elem.tag, token_dict)
        # prev_elem = elem.tag

def fix_heirarchical_bio(token_labels_dict):
    max_num_labels = 0
    # determine the maximum number of labels any token in the citation has
    for (token, labels) in token_labels_dict:
        # print token, labels
        if len(labels) > max_num_labels:
            max_num_labels = len(labels)
    # print

    # for each label index
    for i in range(max_num_labels):
        prev_label_num = -1
        prev_label = ""
        prev_label_list = ["" for m in range(max_num_labels)]
        # print "fixing labels at index ", i
        # go through all the tokens
        for j, (token, labels) in enumerate(token_labels_dict):
            # if the current token has a label at index i, compare it to the previous token's labels at index i to see if the token starts a segment
            if i < len(labels):
                cur_label_num, cur_label = labels[i][0:2], labels[i][2:]
                # print "label for ", token, ": ", cur_label, " with number ", cur_label_num
                if cur_label_num == prev_label_num and cur_label == prev_label:
                    # print "this is token is continuing the segment for this label"
                    labels[i] = "I-" + cur_label
                elif cur_label_num != prev_label_num and cur_label == prev_label:
                    # print "this token is starting a new segment for this label"
                    # if this is the last token and it's starting a new segment, must be U
                    if j == len(token_labels_dict)-1:
                        labels[i] = "U-" + cur_label
                    else:
                        labels[i] = "B-" + cur_label
                    # check if the previous token also started a segment, in which case it should be U and not B
                    if j > 0 and prev_label_list[i].startswith("B-"):
                        # print "changing to U"
                        prev_label_list[i] = "U" + prev_label_list[i][1:]
                else:
                    # print "previous label must not match current label, in which case we're starting a new segment by default"
                    # if this is the last token and it's starting a new segment, must be U
                    if j == len(token_labels_dict) - 1:
                        labels[i] = "U-" + cur_label
                    else:
                        labels[i] = "B-" + cur_label
                    # again, check if previous token started a segment, in which case it should be U and not B
                    if j > 0 and prev_label_list[i].startswith("B-"):
                        # print "changing to U"
                        prev_label_list[i] = "U" + prev_label_list[i][1:]
                token_labels_dict[j] = (token, labels)
                prev_label_num = cur_label_num
                prev_label = cur_label
                prev_label_list = labels
    #     print "\n"
    # print "\nFIXED: "
    # for (token, labels) in token_labels_dict:
    #     print token, labels

    return token_labels_dict


    # cur_token, _, _, cur_label = citation_string_lines[0].split(" ")
    # for i in range(2, len(citation_string_lines)):
    #     next_token, _, _, next_label = citation_string_lines[i]
    #     cur_labels = cur_label.split("/")
    #     next_labels = next_label.split("/")
    #     # go through each label for the current token, and see if the current token starts the segment for that label
    #     for i in range(len(cur_labels)):
    #         if i < len(next_labels):
    #             cur_num, cur_seg = cur_labels[i].split("-")
    #             next_num, next_seg = next_labels[i].split("-")
    #             if cur_num == next_num:



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
                    # citation_dfs(root, '', parsed_file)
                    tokens_dict = []
                    citation_dfs(root, '', tokens_dict)
                    tokens_dict = fix_heirarchical_bio(tokens_dict)
                    for (token, labels) in tokens_dict:
                        parsed_file.write((token + " d d " + "/".join(labels) + "\n").encode('utf8'))
                    parsed_file.write('\n')
                except ET.ParseError:
                    print citation
            parsed_file.flush()
            parsed_file.close()
        print
        print num_dev
        file.close()

parse_file('test_parser.docs')

parse_file('dev.docs')
parse_file('testing.docs')
parse_file('training.docs')





