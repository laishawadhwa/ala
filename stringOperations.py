#Utility functions OCR

#Assembling words

def assemble_word(word):
    assembled_word=""
    for symbol in word.symbols:
        assembled_word+=symbol.text
    return assembled_word

#find blockLocation

def find_block_location(document,word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled_word=assemble_word(word)
                    if(assembled_word==word_to_find):
                        return block.bounding_box

#Finding single word location

def find_word_location(document,word_to_find):
	print("in function")
	for page in document.pages:
		for block in page.blocks:
			for paragraph in block.paragraphs:
				for word in paragraph.words:
					assembled_word=assemble_word(word)
					if(assembled_word==word_to_find):
						print(word.bounding_box)
						return word.bounding_box

#finding compound words location input document object and target word

def find_compound_word_location(document,word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for idx,word in enumerate(paragraph.words):
                    try:
                        assembled_word=assemble_word(word)+ " " + assemble_word(paragraph.words[idx+1])
                        if(assembled_word==word_to_find):
                            return word.bounding_box
                    except:
                        pass

# finding text in a given set of coordinates (bounding box)


def text_within(document,x1,y1,x2,y2): 
    text=""
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
                        max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
                        min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
                        max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
                        if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):
                            text+=symbol.text
                            if(symbol.property.detected_break.type==1 or 
                               symbol.property.detected_break.type==3):
                                text+=' '
                            if(symbol.property.detected_break.type==2):
                                text+='\t'
                            if(symbol.property.detected_break.type==5):
                                text+='\n'
    return text


#finding nearest radius
#@params: document object, search radius, target word for searching neighbourhood

def find_nearest_words(document,word,radius):
    word_bounding_box = find_word_location(document,word)
    text = ""
    if(not word_bounding_box):
        return text
    centroid_x =  ( word_bounding_box.vertices[0].x + word_bounding_box.vertices[2].x )/2
    centroid_y =  ( word_bounding_box.vertices[0].y + word_bounding_box.vertices[2].y )/2
    
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        x_c = (word.bounding_box.vertices[0].x + word.bounding_box.vertices[2].x)/2
                        y_c = (word.bounding_box.vertices[0].y + word.bounding_box.vertices[2].y)/2
                    
                        distance = math.sqrt((x_c-centroid_x)**2 + (y_c-centroid_y)**2)
                        if(distance<=radius):
                            text+=symbol.text
                            if(symbol.property.detected_break.type==1 or 
                               symbol.property.detected_break.type==3):
                                text+=' '
                            if(symbol.property.detected_break.type==2):
                                text+='\t'
                            if(symbol.property.detected_break.type==5):
                                text+='\n'
    
    return text


#find word based on category


def find_required_words(document,input_word,category = 1.0):
    bounding_box_input_word = find_word_location(document,input_word)
    if(bounding_box_input_word):
        width_input_word = bounding_box_input_word.vertices[2].y - bounding_box_input_word.vertices[0].y
        length_input_word = bounding_box_input_word.vertices[2].x - bounding_box_input_word.vertices[0].x

        min_x = bounding_box_input_word.vertices[0].x - length_input_word/2.0
        max_x = bounding_box_input_word.vertices[2].x + category * length_input_word
        min_y = bounding_box_input_word.vertices[0].y - width_input_word/2.0
        max_y = bounding_box_input_word.vertices[2].y + 2.0 * width_input_word

        text = text_within(document,min_x,min_y,max_x,max_y)
        return text


#finding all occurences of a given word

def find_all_word_location(document,word_to_find):
	list_bounding_box = []
	for page in document.pages:
		for block in page.blocks:
			for paragraph in block.paragraphs:
				for word in paragraph.words:
					assembled_word=assemble_word(word)
					if(assembled_word==word_to_find):
						list_bounding_box.append(word.bounding_box)
	return list_bounding_box
