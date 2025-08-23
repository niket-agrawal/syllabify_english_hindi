# Code adapted from code1_hi_text.py, zzz_library_aksh_matra_count.py --- Sidak
# and			devanagari_hi.py									 --- Ansh
# and           IndicPseudoGen.py                                    --- Niket
# see lib_2025 folder

# Ideally, Hindi being such a complex language to rest of the world, we should do it step by step and give plethora of (OBJECTIVE) values to work with rather than simplifying the complexity. My idea is for every word, anyone should see:

# Word, Segments, N-Aksharas, N-Matras, Which_Aksharas_in_which_segment, Which_Matra_in_which_segment, N_conjuncts, Which_Conjunct_in_which_segment, Swars, Vyanjans, SanyuktVyanjans, Orthographic_length, Complexity_metric
# example,
# word: अनुस्वार,
# 	word_segments: ['अ', 'नु', 'स्वा', 'र']
# 	aksharas: अ, न, स व, र
# 	matras: ु, ा
# 	conjuncts: स्व
# 	which_akshara_in_which_segment: [अ,  न,  सव,  र]
# 	which_matra_in_which_segment: [schwa, 'ु', 'ा', schwa]
# 	which_conjunct_in_which_segment: [-, -, स्व, -]
# 	swars: न, स, व, र
# 	vyanjans: अ
# 	sanyunkt_vyanjans (kha, tra, gya, shra): -
# 	orthographic_length: would be composed of simple and objective rules 
# 	word_complexity: heuristic based and informed from models/experimental values
# 	syllables: no idea currently = shabdansh = word segments

import unicodedata
import re
import sys
import os
import tkinter as tk
from tkinter import font as tkFont

# word = the word or segment for which the width is required
# fonttype = family of font (must be installed on PC)
# fontsize = size of font in points (pts.)
def word_width_pixels(word, fonttype, fontsize):
    #pyglet.font.add_file(fonttype)
    root = tk.Tk()
    # list all availiable fonts
    all_fonts = tkFont.families()
    # if(fonttype not in all_fonts):
    #     print("- EXCEPTION:",fonttype,"not found in tkinter fonts !!!")
    #     print("- WARNING: moving ahead with default tkinter font. Beware.")
    txt = tkFont.Font(family=fonttype, size=fontsize)
    width = txt.measure(word)
    root.destroy()
    return (width)

def word_segment_anurag_sascha(word):
    w = word.strip()
    # list of maatraas including halant
    l_m=["ा", "ि", "ी", "ु", "ू", "े", "ै", "ो", "ौ", "ं", "ः", "़", "ृ", "़", "ॄ", "ृ", "ॅ", "्", "ॉ",'ँ'] 
    # list of segments of the word
    l_u=[]
    w_l=len(w)
    x=0
    seg_pos_end=0
    while x<w_l:
        seg_pos_begin=seg_pos_end
        # checks if two consonants are placed next to each other. In such a case, new segment starts with the 2nd consonant.
        if x+1 < w_l and (w[x] in l_m) == False and (w[x+1] in l_m) == False: 
            seg_pos_end = x+1
            seg=w[seg_pos_begin:seg_pos_end]
            l_u.append(seg)
            x=seg_pos_end
        # checks if a maatraa (but not halant) occurs just before a consonant. In such a case, new segment starts with the consonant.
        elif x+1 < w_l and (w[x] in l_m) == True and w[x] != "्" and (w[x+1] in l_m) == False: 
            seg_pos_end = x+1
            seg=w[seg_pos_begin:seg_pos_end]
            l_u.append(seg)
            x=seg_pos_end
            c=0
            m=0
            h=0
        # checks if it is the last segment.
        elif x+1 == w_l: 
            seg=w[seg_pos_begin:]
            l_u.append(seg)
            x=x+1
        else:
            x=x+1
    return (l_u, len(l_u))


def word_segment_niket(word):
	""" Convert shabd(word) to bigrams alongwith its frequency
        code section from wuggy, nshabd
	"""
	index=0
	string = word.strip()
	chars = [s for s in string]
	akshars=[]

	for c in chars:
		temp=unicodedata.name(c)
		akshar=temp.find('DEVANAGARI LETTER',0)
		if akshar!=-1:
			akshars.append(c)
			index=index+1
		else:
			if index!=0:
				akshars[index-1]=akshars[index-1]+c
	return akshars

# https://stackoverflow.com/a/47123580
def word_segment_shantanoo(word):
    """ Generate grapheme clusters for the Devanagari text."""
    stop = '्'
    cluster = u''
    end = None
    for char in word:
        category = unicodedata.category(char)
        if (category == 'Lo' and end == stop) or category[0] == 'M':
            cluster = cluster + char        
        else:
            if cluster:
                yield cluster
            cluster = char
        end = char

    if cluster:
        yield cluster

# DEVANAGARI_VIRAMA = '\u094D'
# NUKTA = '\u093C'
# ZWJ = '\u200D'
# ZWNJ = '\u200C'

# def word_segment_shantanoo(word):
#     """Yield approximate Devanagari grapheme clusters (consonant/virama/marks).
#     Not a full ICU implementation but works for common cases."""
#     cluster = ''
#     prev_was_virama = False

#     for ch in word:
#         cat = unicodedata.category(ch)
#         # Combining marks (vowel signs, matras, anusvara, candrabindu, etc.)
#         if cat.startswith('M') or ch in (NUKTA, ZWJ, ZWNJ):
#             # attach marks, nukta, ZWJ/ZWNJ to current cluster
#             cluster += ch
#             prev_was_virama = False
#             continue

#         # If previous char was virama, attach this consonant to same cluster
#         if prev_was_virama:
#             cluster += ch
#             prev_was_virama = False
#             # if this consonant is followed by virama it will be handled next loop
#             continue

#         # If this is a virama, attach it and remember
#         if ch == DEVANAGARI_VIRAMA:
#             cluster += ch
#             prev_was_virama = True
#             continue

#         # Otherwise, this is a new base (consonant or independent vowel or other)
#         if cluster:
#             yield cluster
#         cluster = ch
#         prev_was_virama = False

#     if cluster:
#         yield cluster



#########################################################################
def string_clean(st):
	st = re.sub(r"ज+्+ञ|त+्+र|क+्+ष|श+्+र","क", st)
	return st
##########################################################################
def character_count(st):
	words=[0]
	matras=[]
	halant=[]
	viram=False
	wcount=0
	count=0
	mcount=0
	for c in st:
		string=unicodedata.name(c)
		#print(c)
		letter=string.find('DEVANAGARI LETTER',0)
		if letter==-1:
			if c=='्' and words[count]=='र' :
				halant.append(c)
				viram=False
				wcount=wcount-1
				mcount=mcount+1
			elif c=='्':
				halant.append(c)
				viram=True
				wcount=wcount-0.5
			else:
				matras.append(c)
				mcount=mcount+1
				viram=False
		else:
			if viram==True and (c=='र' ):
				mcount=mcount+1	
				wcount=wcount+0.5
			
			else:	
				words.append(c)
				wcount=wcount+1
				count=count+1
			viram=False
	return wcount, mcount, halant, words, matras 
###################################################################################################
def count_it(word):
	lst=word.split()
	#print(lst[0])
	if(lst!=[]):
		seq=(lst[0])
		st=''.join(seq)		
		NS=string_clean(st)
		W_count , M_count, halant, words, matras = character_count(NS)
		return(word,W_count,M_count,len(halant),W_count+M_count)
	elif(lst==[]):
		return(word,0,0,0,0)
###################################################################################################

def complex_score_samar_potsdam(word):
    score = 0
    #word = "पब्लिसिटी"
    word = re.sub(r"ज+्+ञ|त+्+र|क+्+ष|श+्+र","Z", word)
    for b in word:
        i = unicodedata.name(b)
        #print(b,i)
        
        ## Appendix A.1, A.4
        vow_i = (i.find('VOWEL SIGN I') == 11) #choti i, cost 1
        vow_ii = (i.find('VOWEL SIGN II') == 11) #choti i, cost 1
        if vow_ii:
            cst = -1
            score = score + cst
        halant = (i.find('VIRAMA') == 16)  #halant, cost 0.5
         ## cannot implement 1+d (for now)

        ## Appendix A.2
        vow_e = (i.find('VOWEL SIGN E') == 11) #a, cost 0.5
        vow_ai = (i.find('VOWEL SIGN AI') == 11) #aiy, cost 0.5
        vow_cb = (i.find('CANDRABINDU') == 16) #chandrabindu, cost 0.5
        vow_anu = (i.find('ANUSVARA') == 16) #only bindu on top, cost 0.5
        vow_ce = (i.find('VOWEL SIGN CANDRA E') == 11) #only chandra on top, cost 0.5
        vow_co = (i.find('VOWEL SIGN CANDRA O') == 11) #matra + only chandra on top, cost 0.5
        ## Appendix A.3
        qa = (i.find('LETTER QA') == 11) #ka with bindi below, cost 0.5
        ka = (i.find('LETTER KHHA') == 11) #kha with bindi below, cost 0.5
        ga = (i.find('LETTER GHHA') == 11) #ga with bindi below, cost 0.5
        ja = (i.find('LETTER ZA') == 11) #jha with bindi below, cost 0.5
        fa = (i.find('LETTER FA') == 11) #fa with bindi below, cost 0.5
        nuk = (i.find('NUKTA')==16)  # bindu on bottom, cost 0.5
        vow_u = (i.find('VOWEL SIGN U') == 11) #choti u, cost 0.5
        vow_uu = (i.find('VOWEL SIGN UU') == 11) #badi uu, cost 0.5
        ## Appendix A.5
        ## cannot implement composite (r for now)
        letter_z = (i.find('LETTER Z') == 14)

        if vow_i:
            cst = 1
        elif halant:
            cst = 0.5
        elif vow_e or vow_ai or vow_cb or vow_anu or vow_ce or vow_co:
            cst = 0.5
        elif qa or ka or ga or ja or fa or nuk:
            cst = 0.5
        elif vow_u or vow_uu:
            cst = 0.5
        elif letter_z:
            cst = 1
        else:
            cst = 0
        score = score + cst
    return score

def complex_score_ark(word):
    score2 = 0
    for b in word:
        i = unicodedata.name(b)
        nuk = i.find('NUKTA')  # bindu on bottom (ignore) cost 0.2
        anu = i.find('ANUSVARA')  # kind of matra (bindu on top) cost 0.3
        cb = i.find('CANDRABINDU')  # kind of matra cost 0.5
        vir = i.find('VIRAMA')  # kind of matra but subtract 1 character if present cost +0.5 -1 = -0.5
        letr = i.find('LETTER')  # all characters cost +1
        vow = i.find('VOWEL')  # all matras cost +0.8
        vis = i.find('VISARGA')  # : kind of matra +0.6
        if nuk == 16:
            cst = 0.2
        elif anu == 16:
            cst = 0.3
        elif cb == 16:
            cst = 0.5
        elif vir == 16:
            cst = -0.5
        elif letr == 11:
            cst = 1
        elif vow == 11:
            cst = 0.4
            if i.find('VOWEL SIGN I') == 11:
                cst = 0.8
            if i.find('VOWEL SIGN II') == 11:
                cst = 0.4
        elif vis == 16:
            cst = 0.4
        else:
            cst = 0  # special case of om
        score2 = score2 + cst
    return score2

def complex_score_niket2025(word):
    score2 = 0
    for b in word:
        i = unicodedata.name(b)
        nuk = i.find('NUKTA')  # bindu on bottom (ignore) cost 0.2
        anu = i.find('ANUSVARA')  # kind of matra (bindu on top) cost 0.3
        cb = i.find('CANDRABINDU')  # kind of matra cost 0.5
        vir = i.find('VIRAMA')  # kind of matra but subtract 1 character if present cost +0.5 -1 = -0.5
        letr = i.find('LETTER')  # all characters cost +1
        vow = i.find('VOWEL')  # all matras cost +0.8
        vis = i.find('VISARGA')  # : kind of matra +0.6
        if nuk == 16:
            cst = 0.5
        elif anu == 16:
            cst = 0.5
        elif cb == 16:
            cst = 0.5
        elif vir == 16:
            cst = -0.5
        elif letr == 11:
            cst = 1
        elif vow == 11:
            cst = 0.5
        elif vis == 16:
            cst = 0.5
        else:
            cst = 0  # special case of om
        score2 = score2 + cst
    return score2

