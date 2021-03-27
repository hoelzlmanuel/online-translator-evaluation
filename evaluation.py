from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.nist_score import corpus_nist
from nltk.translate.meteor_score import meteor_score
from nltk.translate.gleu_score import corpus_gleu
import re
from nltk.translate.ribes_score import corpus_ribes
from nltk.translate.chrf_score import corpus_chrf
from pyter import ter
from copy import deepcopy

translations = {
  "Amazon Translate":
    [
      {
        "translation": "St. Stephen's Cathedral (originally cathedral and metropolitan church of St. Stephen and all Saints) on Vienna's Stephansplatz (district of Inner City) has been a cathedral since 1365 (seat of a cathedral chapter), since 1469/1479 cathedral (bishop's seat) and since 1723 Metropolitan Church of the Archbishop of Vienna",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic cathedral, also known as Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes referred to as the Austrian national sanctuary",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "Its name is Saint Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patrol is All Saints' Day",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 metres long and 34 metres wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the west facade, flanked by the two pagan towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "St. Stephen's Cathedral has four towers: the highest at 136.4 metres is the south tower, the north tower was not completed and is only 68 metres high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In former Austria-Hungary, no church could be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Immaculate Conception Cathedral in Linz was built two meters lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four meters deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which form the main chime of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest free-swinging church bell in Europe, has been located in the north tower under a tower hood from the Renaissance period since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "DeepL":
    [
      {
        "translation": "St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and All Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church (seat of a cathedral chapter) since 1365, a cathedral (bishop's seat) since 1469/1479 and a metropolitan church of the Archbishop of Vienna since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic cathedral, also called Steffl by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "It is named after St. Stephen, the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patron saint is All Saints",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 metres long and 34 metres wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the west façade, flanked by the two pagan towers, which are about 65 metres high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "In total, St. Stephen's Cathedral has four towers: the highest, at 136.4 metres, is the south tower; the north tower was not completed and is only 68 metres high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austro-Hungarian Empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Cathedral of the Assumption in Linz was built two metres lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "The south tower contains a total of 13 bells, eleven of which form the main peal of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era dome since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "Google Translate":
    [
      {
        "translation": "St. Stephen's Cathedral (actually the cathedral and metropolitan church of St. Stephen and all the saints) on Vienna's Stephansplatz (Inner City district) has been the cathedral church (seat of a cathedral chapter) since 1365, the cathedral since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic cathedral, also known as Steffl for short by the Viennese, is a symbol of Vienna and is sometimes referred to as the Austrian national shrine",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "It is named after St. Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patronage is All Saints' Day",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The structure is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the west facade, flanked by the two heather towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "St. Stephen's Cathedral has a total of four towers: the highest at 136.4 meters is the south tower, the north tower was not completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Cathedral of the Conception of Mary in Linz was built two meters lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four meters deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which form the main bell of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest free-swinging church bell in Europe, has been located in the north tower under a tower dome from the Renaissance period since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "Microsoft Translator":
    [
      {
        "translation": "St. Stephen's Cathedral (actually cathedral and metropolitan church in St. Stephen and all saints) on Vienna's Stephansplatz (inner city district) has been a cathedral church (seat of a cathedral chapter) since 1365, a cathedral (bishop's seat) since 1723, and the Metropolitan Church of the Archbishop of Vienna since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic Cathedral, also known by the Viennese as Steffl, is considered a landmark of Vienna and is sometimes referred to as the Austrian national sanctuary",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "The name is given to St. Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patrozinium is All Saints' Day",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The structure is 107 metres long and 34 metres wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the western facade, flanked by the two heath towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "In total, St. Stephen's Cathedral has four towers: the highest one at 136.4 metres is the south tower, the north tower has not been completed and is only 68 metres high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary no church could be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Cathedral of the Nativity of the Virgin Mary in Linz was built two metres lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which form the main bell of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower hood since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "ModernMT":
    [
      {
        "translation": "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) at St. Stephen's Square (district Innere Stadt) has been the cathedral church (seat of a cathedral chapter) since 1365, cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic Cathedral, also called Steffl by the Viennese, is considered a landmark of Vienna and is sometimes referred to as the Austrian National Shrine",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "It is named after St. Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second Patrocinium is All Saints",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor from 1230/40 to 1263 are still preserved and form the western facade, flanked by the two heath towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "The St. Stephen's Cathedral has a total of four towers: the highest with 136.4 meters is the South Tower, the North Tower was not completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary, no church was allowed to be built higher than the South Tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Cathedral of the Conception of the Virgin Mary in Linz was built two metres lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The South Tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the South Tower there are a total of 13 bells, eleven of which make up the main sound of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest freely vibrating church bell in Europe, has been in the North Tower under a Renaissance dome since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "PROMT.One":
    [
      {
        "translation": "The St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and All Saints) at the Viennese St. Stephen's Square (Inner City District) has been a cathedral church (seat of a cathedral chapter) since 1365, cathedral (bishop's seat) since 1469/1479 and metropolitan church of the archbishop since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic Cathedral, also called Steffl for short by the Viennese, is considered a landmark in Vienna and is sometimes referred to as the Austrian national sanctuary",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "The namesake is Saint Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patrol is All Saints",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The structure is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the western facade, flanked by the two pagan towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "In total, St. Stephen's Cathedral has four towers: The highest tower at 136.4 meters is the south tower, the north tower has not been completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In former Austria-Hungary no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Marian Conception Cathedral in Linz was built two metres lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The South Tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four meters deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which form the main vent of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest freely ringing church bell in Europe, has been located in the north tower under a tower hood from the Renaissance period since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "SDL Machine Translation Cloud":
    [
      {
        "translation": "St. Stephen's Cathedral (actually the cathedral and metropolitan church of St. Stephan and all Saints) on Vienna's Stephansplatz (inner city district) has been a cathedral church (seat of a cathedral chapter) since 1365, a cathedral (bishop's seat) since 1723 and a metropolitan church of the archbishop of Vienna since",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic cathedral, also known as Steffl for short by the Viennese, is considered Vienna's landmark and is sometimes called the Austrian National Shrine",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "St. Stephen, who is considered the first Christian martyr, is the name of St. Stephen",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second Patrozinium is all Saints",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late-Roman predecessor building from 1230/1263 to 1940 have still been preserved and form the west facade, flanked by the two heathen towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "St. Stephen's Cathedral has four towers in total: The highest of 136.4 meters is the south tower, the north tower has not been completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Mariana conception cathedral in Linz was built two meters lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The South Tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four meters deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, of which eleven form the main building of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest free-swinging church bell in Europe, has been located in the north tower under a tower from the Renaissance period since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "SYSTRAN Translate":
    [
      {
        "translation": "The St. Stephen's Cathedral (actually the cathedral and metropolitan church of St. Stephen and all the saints) at the Stephansplatz in Vienna (Innere Stadt district) has been the cathedral church (seat of a cathedral chapter) since 1365, the cathedral (bishop's seat) since 1469/1479 and the metropolitan church of the archbishop of Vienna since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic Cathedral, also known as Steffl for short by the Viennese, is regarded as the landmark of Vienna and is sometimes also referred to as the Austrian national sanctuary",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "The name is given to St. Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patrocinium is All Saints",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the west facade, flanked by the two pagan towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "The St. Stephen's Cathedral has four towers: At 136.4 meters the highest is the South Tower, the North Tower has not been completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the cathedral of St. Mary's Conception in Linz was built two meters lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The South Tower is an architectural masterpiece of the time; Despite its remarkable height, the foundation is less than four meters deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which are the main bells of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest free-swinging church bell in Europe, has been located in the North Tower under a Renaissance tower hood since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "Watson Language Translator":
    [
      {
        "translation": "The St. Stephen's Cathedral (Cathedral and Metropolitan Church of St. Stephan and all the saints) at Vienna's Stephansplatz (district of the inner city) has been the cathedral church (seat of a cathedral chapter) since 1365, since 1469/1479 cathedral (bishop's seat) and since 1723 Metropolitan Church of the Archbishop of Vienna",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic Cathedral, also known as Steffl, is known as the landmark of Vienna and is sometimes referred to as the Austrian national sanctuary",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "Its name is Saint Stephen, who is the first Christian martyr to be a martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second Patrozinium is All Saints",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the west facade, flanked by the two Heidenürmen, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "In total, the St. Stephen's Cathedral has four towers: the highest with 136.4 meters is the south tower, the north tower has not been completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Mariä-conception-Dom in Linz was built by two meters lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The south tower is an architectural masterpiece of the time; in spite of its remarkable height, the foundation is less than four metres deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which form the main building of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The pummerin, the third largest free-swinging church bell in Europe, has been located in the north tower under a tower hood dating back to the Renaissance period since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
  "Yandex Translate":
    [
      {
        "translation": "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and All Saints) on Vienna's Stephansplatz (district Inner City) has been cathedral church (seat of a cathedral chapter) since 1365, cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723",
        "references": ["St. Stephen's Cathedral (actually the Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Innere Stadt district) has been a cathedral church since 1365, a cathedral (bishop's see) since 1469/1479 and the metropolitan church of the Archbishop of Vienna since 1723", "St. Stephen's Cathedral (actually Cathedral and Metropolitan Church of St. Stephen and all Saints) on Vienna's Stephansplatz (Inner City district) has been a cathedral church since 1365, a cathedral (bishop's seat) since 1469/1479 and metropolitan church of the Archbishop of Vienna since 1723"]
      },
      {
        "translation": "The Roman Catholic Cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine",
        "references": ["The Roman Catholic cathedral, which is also called Steffl for short by the Viennese, is considered a landmark of Vienna and is also referred to as an Austrian national shrine", "The Roman Catholic cathedral, also called Steffl for short by the Viennese, is considered a landmark of Vienna and is sometimes also referred to as the Austrian national shrine"]
      },
      {
        "translation": "It is named after Saint Stephen, who is considered the first Christian martyr",
        "references": ["The namesake is Saint Stephen, who is said to have been the first Christian martyr", "Saint Stephen, who is considered to be the first Christian martyr, is the namesake of the cathedral"]
      },
      {
        "translation": "The second patrocinium is All Saints ' Day",
        "references": ["The second patronal festival is All Saints' Day", "The second patronal festival is All Saints' Day"]
      },

      {
        "translation": "The building is 107 meters long and 34 meters wide",
        "references": ["The building is 107 meters long and 34 meters wide", "The building is 107 metres long and 34 metres wide"]
      },
      {
        "translation": "The cathedral is one of the most important Gothic buildings in Austria",
        "references": ["The cathedral is one of the most important Gothic buildings in Austria", "The cathedral is one of the most important Gothic buildings in Austria"]
      },
      {
        "translation": "Parts of the Late Romanesque predecessor building from 1230/40 to 1263 are still preserved and form the western facade, flanked by the two pagan towers, which are about 65 meters high",
        "references": ["Parts of the late Romanesque predecessor building dating back to 1230/40 until 1263 are still intact and make up the west facade, flanked by the two pagan towers which are around 65 meters tall", "Parts of the late Romanesque predecessor building from 1230/40 till 1263 are still intact and form the west facade, which is flanked by the two heathen towers that are approximately 65 metres high"]
      },
      {
        "translation": "In total, St. Stephen's Cathedral has four towers: the tallest with 136.4 meters is the south Tower, the north tower has not been completed and is only 68 meters high",
        "references": ["In total, St. Stephen's Cathedral has four towers: With a height of 136.4 meters, the tallest is the south tower, the north tower was never finished and is only 68 meters high", "In total, St. Stephen's cathedral has four towers: The highest one being the south tower with a height of 136.4 metres, the north tower was not completed and is only 68 metres high"]
      },
      {
        "translation": "In the former Austria-Hungary, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral",
        "references": ["In former Austro-Hungary no church was allowed to be built taller than the south tower of St. Stephen's Cathedral", "In the former Austro-Hungarian empire, no church was allowed to be built higher than the south tower of St. Stephen's Cathedral"]
      },
      {
        "translation": "For example, the Cathedral of the Conception of the Virgin Mary in Linz was built two metres lower",
        "references": ["As an example, the Cathedral of the Immaculate Conception in Linz was built two meters lower", "For example, the New Cathedral in Linz was built two metres lower"]
      },

      {
        "translation": "The south Tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four meters deep",
        "references": ["The south tower is an architectural masterpiece of the time; in spite of its remarkable height the foundation is less than four meters deep", "The south tower is an architectural masterpiece of the time; despite its remarkable height, the foundation is less than four metres deep"]
      },
      {
        "translation": "In the south tower there are a total of 13 bells, eleven of which form the main ringing of St. Stephen's Cathedral",
        "references": ["In the south tower there are a total of 13 bells, eleven of which make up the main bells of St. Stephen's Cathedral", "There are 13 bells located in the south tower, eleven of which form the main chime of St. Stephen's cathedral"]
      },
      {
        "translation": "The Pummerin, the third largest free-swinging church bell in Europe, has been located in the North Tower under a Renaissance-era tower hood since 1957",
        "references": ["The Pummerin, the third largest free-swinging rung church bell of Europe, is located in the north tower since 1957 beneath a dome from the Renaissance period", "The Pummerin, the  third-largest free-swinging church bell in Europe, has been located in the north tower under a Renaissance-era tower dome since 1957"]
      },
    ],
}

translations2 = deepcopy(translations)

for translation in translations:
  for sentence in translations[translation]:
    sentence["translation"] = sentence["translation"].replace(".", " . ").split()
    for idx, reference in enumerate(sentence["references"]):
      sentence["references"][idx] = reference.replace(".", " . ").split()

for service in translations:
  print(service)
  hypotheses_split = [translations[service][0]["translation"], translations[service][1]["translation"]]
  references_split = [translations[service][0]["references"], translations[service][1]["references"]]

  hypotheses = [translations2[service][0]["translation"], translations2[service][1]["translation"]]
  references = [translations2[service][0]["references"], translations2[service][1]["references"]]

  # BLEU, 0 = bad, 1 = good

  print("BLEU: " + str(corpus_bleu(references_split, hypotheses_split)))

  # NIST

  print("NIST: " + str(corpus_nist(references_split, hypotheses_split, 3)))

  # METEOR

  avg_score = 0
  for idx, hypothesis in enumerate(hypotheses):
    avg_score += meteor_score(references[idx], hypothesis)
  avg_score /= len(hypotheses)
  print("METEOR: " + str(avg_score))

  # GLEU

  print("GLEU: " + str(corpus_gleu(references_split, hypotheses_split)))

  # TER

  refs_split = [[], []]
  for reference in references_split: # all elements in references_split have to have the same length
    for idx in range(len(reference)):
      refs_split[idx].append(reference[idx])

  avg_score = 0
  for ref in refs_split:
    for r, hyp in zip(ref, hypotheses_split):
      avg_score += ter(r, hyp)
  avg_score /= len(refs_split)
  avg_score /= len(hypotheses)
  print("TER: " + str(avg_score))

  # RIBES

  print("RIBES: " + str(corpus_ribes(references_split, hypotheses_split)))

  # ChrF

  avg_score = 0
  for ref in refs_split:
    avg_score += corpus_chrf(ref, hypotheses_split)
  avg_score /= len(refs_split)
  print("ChrF: " + str(avg_score))

  print("")