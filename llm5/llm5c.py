import numpy as np
import llm5_util as llm5
from autocorrect import Speller
from pattern.text.en import singularize

########################## add llm5_util.py and llm5_short.py to appendix
########################## crawl my books char char 
########################### identify \index{xxx} and \section \subsection \subsubsection ; for each index add list of section / chapters / books
##########################      use it to complement my LLM

####### twitter2.xlsx on google drive, and DSC-master-capri5.xlsx
#######  Wikipedia directory: wikipedia.org/wiki/Category:Machine_learning (+ indexes)
####### poor : https://en.wikipedia.org/wiki/Category:Statistics


#--- [1] some utilities
########################### put some of them in library

# words can not be any of these words
stopwords = ( "of", "now", "have", "so", "since", "but", "and", 
              "thus", "therefore", "a", "as", "it", "then", "that",
              "with", "to", "is", "will", "the", "if", "there", "then,",
              "such", "or", "for", "be", "where", "on", "at", "in", "can",
              "we", "on", "this", "let", "an", "are", "has", "how", "do",
              "each", "which", "nor", "any", "all", "al.", "by", "having",
              "therefore", "another", "having", "some", "obtaining",
              "into", "does", "union", "few", "makes", "occurs", "were",
              "here", "these", "after", "defined", "takes", "therefore,",
              "here,", "note", "more", "considered", "giving", "associated", 
              "etc.", "i.e.,", "Similarly,", "its", "from", "much", "was",
              "given", "Now,", "instead", "above,", "rather", "consider",
              "found", "according", "taking", "proved", "now,", "define",
              "showed", "they", "show", "also", "both", "must", "about",
              "letting", "gives", "their", "otherwise", "called", "descibed",
              "related", "content", "eg", "needed", "picks", "yielding",
              "obtained", "exceed", "until", "complicated", "resulting",
              "give", "write", "directly", "good", "simply", "direction",
              "when", "itself", "ie", "al", "usually", "whose", "being",
              "so-called", "while", "made", "allows", "them", "would", "keeping",
              "denote", "implemented", "his", "shows", "chosen", "just",
              "describes", "way", "stated", "follows", "approaches", "known",
              "result", "sometimes", "corresponds", "every", "referred",
              "produced", "than", "may", "not", "exactly", "&nbsp;", "whether",
              "illustration", ",", ".", "...", "states", "says", "known", "exists",
              "expresses", "respect", "commonly", "describe", "determine", "refer",
              "often", "relies", "used", "especially", "interesting", "versus",
              "consists", "arises", "requires", "apply", "assuming", "said",
              "depending", "corresponding", "calculated", "depending", "associated",
              "corresponding", "calculated", "coincidentally", "becoming", "discussion",
              "varies", "compute", "assume", "illustrated", "discusses", "notes",
              "satisfied", "terminology", "scientists", "evaluate", "include", "call",
              "implies", "although", "selected", "however", "between", "explaining",
            )

############################# upload all new tables on GitHub after adding stopwords

# map below to deal with some accented / non-standard characters
utf_map = { "&nbsp;"   : " ", 
            "&oacute;" : "e",
            "&eacute;" : "e",
            "&ouml;"   : "o",
            "&ocirc;"  : "o",
            "&#233;"   : "e",
            "  "       : " ",
            "'s"       : "",   # example: Feller's --> Feller
          }

def get_top_category(page):

    # useful if working with all top categories rather than just one 
    # create one set of tables (dictionary, ngrams...) for each top category
    # here we mostly have only one top category: 'Probability & Statistics'
    # possible cross-links between top categories (this is the case here)

    read = (page.split("<ul class=\"breadcrumb\">"))[1]
    read = (read.split("\">"))[1]
    top_category = (read.split("</a>"))[0]
    return(top_category)


def trim(word):
    return(word.replace(".", "").replace(",",""))


def split_page(row):

    line = row.split("<!-- Begin Content -->")  
    header = (line[0]).split("\t~")
    header = header[0]
    html = (line[1]).split("<!-- End Content -->")
    content = html[0] 
    related = (html[1]).split("<h2>See also</h2>")
    if len(related) > 1:
        related = (related[1]).split("<!-- End See Also -->")
        related = related[0]
    else:
        related = ""
    see = row.split("<p class=\"CrossRefs\">")
    if len(see) > 1:
        see = (see[1]).split("<!-- Begin See Also -->")
        see = see[0]
    else:
        see = ""
    return(header, content, related, see) 


def list_to_text(list):

    text = " " + str(list) + " "
    text = text.replace("'", " ")
    text = text.replace("\"", " ")
    text = text.replace("-", " ")
    text = text.replace("(", "( ")
    text = text.replace(")", ". )")
    text = text.lower()
    return(text)


### def xxxreject(word, stopwords):

    ######## detect stopwords in high frequency words (multi token) ##############################
    # import NLTK (natural language toolkit) #############################
    # from nltk.corpus import stopwords 
    # nltk.download('stopwords')
    # print(stopwords.words('english')) ##############################

    ######## ad-hoc stoplist and flaglist for each site / category
    ###### even, real, strong, large, one should not be stop words
    ######## enable search by category ############### !!! [process category table from list_urls]
    #####         add top category to url_list
    #####         assign category to future pages not on Wolfram
    ######## use wolfram crawl to start with stackexchange
    ###### keep all n-grams, no standardization (plural to singular)
    ######## keep capitalization, commas and points (.)
    ######## Lemmatization and stemming are the techniques of keyword normalization, while Levenshtein and Soundex are techniques of string matching.
    ##             https://en.wikipedia.org/wiki/Edit_distance
    ##             https://huggingface.co/tasks/sentence-similarity
    ##             https://en.wikipedia.org/wiki/Semantic_similarity
    #### in stackexchange, use tags to extend categoriries // use top words
    ######## accept advertisers in my LLM app / add fake ones initially, with utm


#--- [2] core function to create/update dictionary and satellite tables
###################### put them in a library ################
######################## put all tables into an object ###########


#--- [3] Read Wolfram crawl and update main tables

### read from URL: [mention it in document] ##########################
#### https://github.com/VincentGranville/Large-Language-Models/raw/main/crawl_final_stats.txt.gz

file_html = open("crawl_final_stats.txt","r",encoding="utf-8")
Lines = file_html.readlines() 

# unless otherwise specified, a word consists of 1, 2, 3, or 4 tokens

dictionary = {}              # words with counts
word_pairs = {}              # pairs of 1-token words found in same word, with count
url_map = {}                 # URL IDs attached to words in dictionary
arr_url = []                 # maps URL IDs to URLs (one-to-one)
hash_category = {}           # categories attached to a word
hash_related = {}            # related topics attached to a word
hash_see = {}                # topics from "see also" section, attached to a word
word_list = {}               # list of 1-token words associated to a 1-token word 

word_count = 0 ############### do we need this ???
url_ID = 0  # init for first crawled page

# process content from Wolfram crawling, one page at a time
# for Probability & Statistics category

for row in Lines:

    #-- cleaning; each row is a full web page + extra info

    for key in utf_map:
        row = row.replace(key, utf_map[key])

    (header, content, related, see) = split_page(row)
    url = (header.split("\t"))[0] 
    category = (header.split("\t"))[1]
    # top_category not always "Probability & Statistics"
    top_category = get_top_category(row)

    # processing "related content" on web page
    list = related.split("\">")
    related = ()
    for item in list:
        item = (item.split("<"))[0]
        if item != "" and "mathworld" not in item.lower():
            related = (*related, item)

    # processing "see also" on web page
    if see != "":
        list = see.split("\">")
        see = ()
        for item in list:
            item = (item.split("<"))[0]
            if item != "" and item != " ":
                see = (*see, item)
   
    text_category = list_to_text(category)
    text_related = list_to_text(related)
    text_see = list_to_text(see)
    content += text_category + text_related + text_see

    # skip all chars between 2 quotes (it's just HTML code)
    flag = 0
    cleaned_content = ""
    for char in content:
        if char == "\"":
            flag = 1 - flag
        if flag == 0:
            cleaned_content += char

    cleaned_content = cleaned_content.replace(">", "> ")
    cleaned_content = cleaned_content.replace("<", ". <")
    cleaned_content = cleaned_content.replace("(", "( ")
    cleaned_content = cleaned_content.replace(")", ". )")
    cleaned_content = cleaned_content.lower()
    data = cleaned_content.split(" ")
    stem_table = llm5.stem_data(data, stopwords, dictionary)

    # update tables after each parsed webpage
    # data is an array containing cleaned words found in webpage

    url_ID = llm5.update_core_tables(data, dictionary, url_map, arr_url, hash_category, 
                                     hash_related, hash_see, stem_table, category, url, 
                                     url_ID, stopwords, related, see, word_pairs, word_list)

########################## more stopwords needed ######################


#--- [4] create embeddings and ngrams tables, once all sources are parsed

pmi_table               = llm5.create_pmi_table(word_pairs, dictionary)    
embeddings              = llm5.create_embeddings(word_list, pmi_table)
ngrams_table            = llm5.build_ngrams(dictionary)
compressed_ngrams_table = llm5.compress_ngrams(dictionary, ngrams_table)

#--- [5] print some stats (utilities)

def cprint(title, list, output_file, labels = ""):
#########################  add sponsored section ###############
    clist = llm5.collapse_list(list)
    print("\n%s\n" %(title))
    output_file.write("\n%s\n\n" %(title))
    if labels != "":
        print(labels + "\n")
        output_file.write(labels)
    for item in clist:
        if title == "URLs":
            # here clist is a list of URL IDs
            url = arr_url[item]  
            print(clist[item], url)
            output_file.write(str(clist[item]) + " " + url + "\n")
        elif str(item) != '()':
            print(clist[item], item)
            output_file.write(str(clist[item]) + " " + str(item) + "\n")
    return()


def word_summary(word, ccnt1, ccnt2, threshold, output_file):

    if word not in dictionary:
        print("No result")
        output_file.write("No result\n")
        cnt = 0
    else:   
        cnt = dictionary[word]

    if cnt > ccnt1:

        print("----------------------------------------------")
        output_file.write("----------------------------------------------\n")
        print(word, dictionary[word])
        output_file.write(word + " " + str(dictionary[word]) + "\n")
        cprint("URLs", url_map[word], output_file)
        cprint("CATEGORIES & LEVELS", hash_category[word], output_file) 
        related_list = llm5.merge_list_of_lists(hash_related[word])
        cprint("RELATED", related_list, output_file)
        cprint("ALSO SEE", hash_see[word], output_file)

        if word in word_list and word in embeddings:

            # print embedding attached to word

            print_embeddings = {}
            wlist = llm5.collapse_list(word_list[word])
            embedding_list = embeddings[word]

            for word2 in embedding_list:
               if word2 != word:
                   pmi = embedding_list[word2]
                   count = wlist[word2]
                   product = pmi * count
                   string = "%6.2f %6d %7.2f %s" % (pmi, count, product, word2)
                   print_embeddings[string] = (product, count)
 
            print_embeddings = dict(sorted(print_embeddings.items(), 
                                    key=lambda item: item[1], reverse=True))
            print("\nSORTED EMBEDDING\n")
            output_file.write("\nSORTED EMBEDDING\n\n")
            print("   pmi weight    prod token\n")
            output_file.write("   pmi weight    prod token\n\n")
            for embedding in print_embeddings:
                (product, count) = print_embeddings[embedding]
                if count > ccnt2 and product > threshold:
                    print(embedding)
                    output_file.write(embedding + "\n")
    print()
    return()


#--- [6] main loop 

def save_tables(): 
   
    list = { "dictionary" : dictionary,
             "ngrams_table" : ngrams_table,
             "compressed_ngrams_table" : compressed_ngrams_table,
             "word_list" : word_list,
             "embeddings" : embeddings,
             "url_map" : url_map,
             "hash_category" : hash_category,
             "hash_related" : hash_related,
             "hash_see" : hash_see,
           }

    for table_name in list:
        file = open("llm5_" + table_name + ".txt", "w")
        table = list[table_name]
        for word in table:
            file.write(word + "\t" + str(table[word]) + "\n")
        file.close()

    file = open("llm5_arr_url.txt", "w")
    for k in range(0, len(arr_url)):
        file.write(str(k) + "\t" + arr_url[k] + "\n")
    file.close()

    file = open("stopwords.txt","w")
    file.write(str(stopwords))
    file.close()
    file = open("utf_map.txt","w")
    file.write(str(utf_map))
    file.close()

    ################### Names : start with capital but not in position #1 in multi-token word

    return()


dump = False  # to save all potential query results (big file)
save = True   # to save all tables

if save:
    save_tables()
 
if dump:

    # hperparameters
    ccnt1 = 0  # 5
    ccnt2 = 0  # 1
    threshold = 0.0 # 8.0
    
    dump_file = open("llm5_dump.txt", "w")
    for word in dictionary:
        word_summary(word, ccnt1, ccnt2, threshold, dump_file)
    dump_file.close()
     
print("Words (up to 4 tokens):", len(dictionary))
print("1-token words with a list:", len(word_list))
print("1-token words with an embedding:", len(embeddings))


#--- [7] process sample user queries

def process_query(query, ccnt1, ccnt2, threshold, output_file = ""):
    # query is a sorted word, each token is in dictionary
    # retrieve all sub-ngrams with a dictionary entry, print results for each one

    get_bin = lambda x, n: format(x, 'b').zfill(n)
    n = len(query)

    for k in range(1, 2**n): 

        binary = get_bin(k, n)
        sorted_word = ""
        for k in range(0, len(binary)):
            if binary[k] == '1':
                if sorted_word == "":
                    sorted_word = query[k]
                else:
                    sorted_word += "~" + query[k]

        if sorted_word in compressed_ngrams_table:
            list = compressed_ngrams_table[sorted_word]
            # the word below (up to 4 tokens) is in the dictionary
            word = list[0]
            print("Found:", word)
            output_file.write("Found:" + word + "\n")
            word_summary(word, ccnt1, ccnt2, threshold, output_file)
            
    ###############  kw = binomial to identify stopwords
    ############# err on safety: not too many stopwords, user can have its own list
    ############      or self-learning: add/remove stopwords to see improvement
    ########### new detect categories / baysian is weak
    #########3 illustrate with linear regression
    ########## create short version that reads all pre-computed tables; add option to save table in this version
    ######                 one set of tables per main category
    #####################3 for each word attach category list [done?] for each new word (book) find category or create new one
    #################### in category output, the number at the right is the category level
    ##########3 make access to the LLM tables pay-per-use or pay-per-month
    ################# MLT/DSC article: 3 gen ai web api [see LI newsletter]

    return()
   

# hyperparameters
ccnt1     = 0  
ccnt2     = 0   # 2  
threshold = 0   # 8.0  

spell = Speller(lang='en') ############3


query = " "
print("\n")
output_file = open("llm5_results.txt", "w")

while query != "":  

    # entries separated by commas are treated independently
    query = input("Enter queries (ex: Gaussian distribution, central moments): ") 
    queries = query.split(',')
    token_list = []
    token_clean_list = []

    for query in queries:

        tokens = query.split(' ')
        for token in tokens:
            # note: spell('feller') = 'seller', should not be autocorrected
            token = token.lower()
            if token not in dictionary:
                token = spell(token) 
            token_list.append(token)
        stemmed = llm5.stem_data(token_list, stopwords, dictionary, mode = 'Internal')   

        for old_token in stemmed:
            token = stemmed[old_token]
            if token in dictionary:
                token_clean_list.append(token)
        token_clean_list.sort()

        if not token_clean_list: 
            if query != "":
                print("No match found")
                output_file.write("No match found\n")
        else:
            print("Found: ", token_clean_list) 
            output_file.write("Found: " + str(token_clean_list) + "\n") 
            process_query(token_clean_list, ccnt1, ccnt2, threshold, output_file)

output_file.close()

##########3 save results in file
############# Ability to enter multiple queries at once; and to choose category (rather than guessing user intent) [maybe
#     even accept input like this (even as text file): query1 | category1, query2 | category2
#     enter your parameters, monetize with Ads / return embeddings, related, urls, categories...
#     use pmi x weight rather than proba for word embeddings
#     case sensitive, dots comma parenthesis smartly used / minimum rather than heavy cleaning yet better, richer results! 
#     allow you to see what the algo found low quality as sometimes it's great
#     minimum stemming, token order preserved in dictionary

########## in LLM5_short.py , make tables stored privately, pay to access these password-protected tables
#######          for instance, put them on GDrive and you pay to get the link
######### compare google query / wolfram query / my LLM / gpt
##  cosine distance based on correls
######  crawl my books to extend dictionary / merge dictionaries [wolfram + my books]
##          including project textbook + glossary
###### use real english dictionary for mapping [do search english dictionary python
### add [wiki] from my books, brow PDF version of other ML books or big government repository Internet markdown
    
## create left embeddings in addition to right ones ?? NO done at the end with n-gram on user request

#querry = "empirical distribution" "berry" ## "Entropy" # "Convolution" # "Spectral analysis" # "time series" # "Autocorrelation" ### "Maximum"  # "Outlier" # "Extreme"  #  "Range"  ### "Markov"   ### "Beta"

######### add categories: Applied Mathematics / Calculus and Analysis / Discrete Mathematics
########## uppercase important
#### weak for bayesian analysis


