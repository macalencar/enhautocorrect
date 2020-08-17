# -*- coding: utf-8 -*-
#This regex structure allow to identify words like:
# word
# word-word
# word-word-word-...
# word'word
#
#GENERIC REGEX: r"([<ALPHABETH>]+(('[<ALPHABETH>]+)|(-[<ALPHABETH>]+)*)*)"
# 

word_regexes = {
    'en': r"([a-záéè]+(('[a-záéè]+)|(-[a-záéè]+)*)*)",
    'pt-br': r"([a-zãõçáéíóúâêôàü]+(('[a-zãõçáéíóúâêôàü]+)|(-[a-zãõçáéíóúâêôàü]+)*)*)"
}

alphabets = {
    'en': 'abcdefghijklmnopqrstuvwxyzáéè\-\'',
    'pt-br': 'abcdefghijklmnopqrstuvwxyzçáàãâéêèeíóôõússs\-\'',
}

""" 
### LETTER FROM SEVERAL ALPHABETS BASED ON THE SOURCE LANGUAGE ### (Source: Wikipedia)
ABCDEFGHIJKLMNOPQRSTUVWXYZ (Latin alphabet)
    and no other – English, Indonesian, Latin, Malay, Swahili, Zulu
    àéëïĳ – Dutch (Except for the ligature ĳ, these letters are very rare in Dutch. Even fairly long Dutch texts often have no diacritics.)
    áêéèëïíîôóúû Afrikaans
    êôúû – West Frisian
    ÆØÅæøå – Danish, Norwegian
    single diacritics, mostly umlauts
        ÄÖäö – Finnish (BCDFGQWXZÅbcfgqwxzå only found in names and loanwords, occasionally also ŠšŽž)
        ÅÄÖåäö – Swedish (occasionally é)
        ÄÖÕÜäöõü – Estonian
        ÄÖÜäöüß – German (ẞ never at the beginning of a word, unless it is completly written in capitals)
    Circumflexes
        ÇÊÎŞÛçêîşû – Kurdish
        ĂÎÂŞŢăîâşţ – Romanian
        ÂÊÎÔÛŴŶÁÉÍÏâêîôûŵŷáéíï – Welsh; (ÓÚẂÝÀÈÌÒÙẀỲÄËÖÜẄŸóúẃýàèìòùẁỳäëöüẅÿ used also but much less commonly)
        ĈĜĤĴŜŬĉĝĥĵŝŭ – Esperanto
    Three or more types of diacritics
        ÇĞİÖŞÜğçıöşü – Turkish
        ÁÐÉÍÓÚÝÞÆÖáðéíóúýþæö – Icelandic
        ÁÉÍÓÖŐÚÜŰáéíóöőúüű – Hungarian
        ÀÇÉÈÍÓÒÚÜÏàçéèíóòúüï· – Catalan
        ÀÂÇÉÈÊËÎÏÔŒÙÛÜŸàâçéèêëîïôœùûüÿ – French; (diacritics on uppercase characters are often optional; Ÿ and ÿ are found only in certain proper names)
        ÁÀÇÉÈÍÓÒÚËÜÏáàçéèíóòúëüï (· only in Gascon dialect) – Occitan
        ÁÉÍÓÚÂÊÔÀãõçáéíóúâêôà (ü Brazilian and k, w and y not in native words) – Portuguese
    ÁÉÍÑÓÚÜáéíñóúü ¡¿ – Spanish
    ÀÉÈÌÒÙàéèìòù – Italian
    ÁÉÍÓÚÝÃẼĨÕŨỸÑG̃áéíóúýãẽĩõũỹñg̃ - Guarani (the only language to use g̃)
    ÁĄĄ́ÉĘĘ́ÍĮĮ́ŁŃ áąą́éęę́íįį́łń (FQRVfqrv not in native words) – Southern Athabaskan languages
        ’ÓǪǪ́ āą̄ēę̄īį̄óōǫǫ́ǭúū – Western Apache
        'ÓǪǪ́ óǫǫ́ – Navajo
        ’ÚŲŲ́ úųų́ – Chiricahua/Mescalero
    ąłńóż Lechitic languages
        ćęśź Polish
        ćśůź Silesian
        ãéëòôù Kashubian
    A, Ą, Ã, B, C, D, E, É, Ë, F, G, H, I, J, K, L, Ł, M, N, Ń, O, Ò, Ó, Ô, P, R, S, T, U, Ù, W, Y, Z, Ż – Kashubian
    ČŠŽ
        and no other – Slovene
        ĆĐ – Bosnian, Croatian, Serbian Latin
        ÁĎÉĚŇÓŘŤÚŮÝáďéěňóřťúůý – Czech
        ÁÄĎÉÍĽĹŇÓÔŔŤÚÝáäďéíľĺňóôŕťúý – Slovak
        ĀĒĢĪĶĻŅŌŖŪāēģīķļņōŗū – Latvian; (ŌŖ and ōŗ no longer used in most modern day Latvian)
        ĄĘĖĮŲŪąęėįųū – Lithuanian
        ĐÀẢÃÁẠĂẰẲẴẮẶÂẦẨẪẤẬÈẺẼÉẸÊỀỂỄẾỆÌỈĨÍỊÒỎÕÓỌÔỒỔỖỐỘƠỜỞỠỚỢÙỦŨÚỤƯỪỬỮỨỰỲỶỸÝỴ đàảãáạăằẳẵắặâầẩẫấậèẻẽéẹêềểễếệìỉĩíịòỏõóọồổỗốơờởỡớợùủũúụưừửữứựỳỷỹýỵ – Vietnamese
        ꞗĕŏŭo᷄ơ᷄u᷄ – Middle Vietnamese
    ā ē ī ō ū – May be seen in some Japanese texts in Rōmaji or transcriptions (see below) or Hawaiian and Māori texts.
    é – Sundanese
    ñ - Basque

ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي Arabic script
    Arabic, Malay (Jawi), Kurdish (Soranî), Panjabi / Punjabi, Pashto, Sindhi, Urdu, others.
    پ چ ژ گ – Persian (Farsi)

Brahmic family of scripts
    Bengali script
        অ আ কা কি কী উ কু ঊ কূ ঋ কৃ এ কে ঐ কৈ ও কো ঔ কৌ ক্ কত্‍ কং কঃ কঁ ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম য র ৰ ল ৱ শ ষ স হ য় ড় ঢ় ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯
        used to write Bengali and Assamese.
        Devanāgarī
            अ प आ पा इ पि ई पी उ पु ऊ पू ऋ पृ ॠ पॄ ऌ पॢ ॡ पॣ ऍ पॅ ऎ पॆ ए पे ऐ पै ऑ पॉ ऒ पॊ ओ पो औ पौ क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल ळ व श ष स ह ० १ २ ३ ४ ५ ६ ७ ८ ९ प् पँ पं पः प़ पऽ
            used to write, either along with other scripts or exclusively, several Indian languages including Sanskrit, Hindi, Maithili, Magahi Marathi, Kashmiri, Sindhi, Bhili, Konkani, Bhojpuri and Nepali from Nepal.
    Gurmukhi
        ਅਆਇਈਉਊਏਐਓਔਕਖਗਘਙਚਛਜਝਞਟਠਡਢਣਤਥਦਧਨਪਫਬਭਮਯਰਲਲ਼ਵਸ਼ਸਹ
        primarily used to write Punjabi as well as Braj Bhasha, Khariboli (and other Hindustani dialects), Sanskrit and Sindhi.
    Gujarati script
        અ આ ઇ ઈ ઉ ઊ ઋ ઌ ઍ એ ઐ ઑ ઓ ઔ ક ખ ગ ઘ ઙ ચ છ જ ઝ ઞ ટ ઠ ડ ઢ ણ ત થ દ ધ ન પ ફ બ ભ મ ય ર લ ળ વ શ ષ સ હ ૠ ૡૢૣ
        used to write Gujarati and Kachchi
    Tibetan script
        ཀ ཁ ག ང ཅ ཆ ཇ ཉ ཏ ཐ ད ན པ ཕ བ མ ཙ ཚ ཛ ཝ ཞ ཟ འ ཡ ར ལ ཤ ས ཧ ཨ
        used to write Standard Tibetan, Dzongkha (Bhutanese), and Sikkimese

АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШ (Cyrillic alphabet)
    ЙЩЬЮЯ
        Ъ – Bulgarian
        ЁЫЭ
            Ў, no Щ, І instead of И (Ґ in some variants) – Belarusian
            rarely Ъ – Russian
        ҐЄІЇ – Ukrainian
    ЉЊЏ, Ј instead of Й (Vuk Karadžić's reform)
        ЃЌЅ – Macedonian
        ЋЂ – Serbian
    ЄꙂꙀЗІЇꙈОуꙊѠЩЪꙐЬѢЮꙖѤѦѨѪѬѮѰѲѴҀ – Old Church Slavonic, Church Slavonic
    Ӂ – Romanian in Transnistria (elsewhere in Latin)

ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ αβγδεζηθικλμνξοπρσςτυφχψω (Greek Alphabet) – Greek

אבגדהוזחטיכלמנסעפצקרשת  (Hebrew alphabet)
    and maybe some odd dots and lines above, below, or inside characters – Hebrew
    פֿ; dots/lines below letters appearing only with א,י, and ו – Yiddish
    no dots or lines around the letters, and more than a few words end with א (i.e., they have it at the leftmost position) – Aramaic
    Ladino

漢字文化圈 – Some East Asian Languages
    and no other – Chinese
    with あいうえおの Hiragana and/or アイウエオノ Katakana – Japanese

위키백과에 (note commonplace ellipses and circles) Korean

ㄅㄆㄇㄈㄉㄊㄋㄌㄍㄎㄏ etc. -- ㄓㄨˋㄧㄣㄈㄨˊㄏㄠˋ (Bopomofo)
    ㄪㄫㄬ -- not Mandarin

កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមសហយរលឡអវអ្កអ្ខអ្គអ្ឃអ្ងអ្ចអ្ឆអ្ឈអ្ញអ្ឌអ្ឋអ្ឌអ្ឃអ្ណអ្តអ្ថអ្ទអ្ធអ្នអ្បអ្ផអ្ពអ្ភអ្មអ្សអ្ហអ្យអ្រអ្យអ្លអ្អអ្វ អក្សរខ្មែរ (Khmer alphabet) - Khmer

Ա Բ Գ Դ Ե Զ Է Ը Թ Ժ Ի Լ Խ Ծ Կ Հ Ձ Ղ Ճ Մ Յ Ն Շ Ո Չ Պ Ջ Ռ Ս Վ Տ Ր Ց Ւ Փ Ք Օ Ֆ (Armenian alphabet) – Armenian

ა ბ გდ ევ ზ ჱ თ ი კ ლ მ ნ ჲ ო პ ჟ რ ს ტ ჳ უ ფ ქ ღ ყ შ ჩ ც ძ წ ჭ ხ ჴ ჯ ჰ ჵ ჶ ჷ ჸ (Georgian alphabet) – Georgian

AEIOUHKLMNPW' Hawaiian alphabet - Hawaiian
"""
