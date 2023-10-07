from PIL import Image, ImageFont, ImageDraw
import pathlib

def createImage(data, saveName):
    image = Image.new(mode = 'RGB', size = (125 * len(data['groups']) + 30, 200 * (len(data) - 2) + 40), color = 'white')

    imageDraw = ImageDraw.Draw(image)
    groups = data['groups']

    #начальная разметка и текст(
    imageDraw.rectangle((0, 0, image.size[0], image.size[1]), fill='white', outline=(0, 0, 0))
    imageDraw.text((image.size[0] / 2, 11), data['date'], anchor="mm", font = ImageFont.truetype('roboto.ttf', 16), fill = (0, 0, 0))
    
    imageDraw.line((0, 20, image.size[0], 20), fill='Black', width=2)
    for i in range(len(groups)):
        fontSize = 16
        if(len(str(groups[i])) >= (125 / 16 * 1.6)):
            
            fontSize = round(125/(len(str(groups[i])) / 1.7))

        imageDraw.line((30 + 125 * i, 20, 30 + 125 * i, image.size[1]), fill='Black', width=2)
        imageDraw.text((95 + 125 * i, 31), str(groups[i]), anchor="mm", font = ImageFont.truetype('roboto.ttf', fontSize), fill = (0, 0, 0))

    for i in range(len(data) - 2):
        imageDraw.line((0, 40 + 200 * i, image.size[0], 40 + 200 * i), fill='Black', width=2)
        imageDraw.text((15, 140 + 200 * i), str(i + 1), anchor="mm", font = ImageFont.truetype('roboto.ttf', 32), fill = (0, 0, 0))
    #)

    #ячейки
    for column in range(len(groups)):
        for row in range(len(data) - 2):
            if(data[row + 1][column + 1] == []):
                data[row + 1][column + 1].append('')

            if(len(data[row + 1][column + 1]) == 1):

                text = data[row + 1][column + 1][0]
                fontSize = 12
                if(len(text) >= 200):
                    fontSize = 9

                text = text.split('\n')

                for a in range(len(text)):
                    line = text[a]

                    if(len(line) <= (125 / fontSize * 1.7)):
                        continue

                    else:
                        line = list(line)
                        hyphenationList = []

                        for i in range(len(line)):
                            i += 1
                            if(i % int(125 / fontSize * 1.7) == 0):
                                hyphenationList.append(i)
                        
                        for position in hyphenationList:
                            line.insert(position, '\n')
                        
                        newLine = ''
                        for letter in line:
                            newLine += letter

                        text[a] = newLine

                newText = ''
                for i in range(len(text)):
                    line = text[i]

                    if(i >= len(text) - 1):
                        newText += line

                    else:
                        newText += line + '\n'

                imageDraw.text((95 + 125 * column , 140 + 200 * row), newText, anchor="mm", font = ImageFont.truetype('roboto.ttf', fontSize), fill = (0, 0, 0))

            else:
                imageDraw.line((125 * column + 30, 140 + 200 * row, 125 * column + 155, 140 + 200 * row), fill='Black', width=2)
                
                for x in range(2):
                    text = data[row + 1][column + 1][x]
                    text = text.split('\n')

                    for a in range(len(text)):
                        line = text[a]

                        if(len(line) <= (125 / 11 * 1.6)):
                            continue

                        else:
                            line = list(line)
                            hyphenationList = []

                            for i in range(len(line)):
                                i += 1
                                if(i % int(125 / 11 * 1.6) == 0):
                                    hyphenationList.append(i)
                            
                            for position in hyphenationList:
                                line.insert(position, '\n')
                            
                            newLine = ''
                            for letter in line:
                                newLine += letter

                            text[a] = newLine

                    newText = ''
                    for i in range(len(text)):
                        line = text[i]

                        if(i >= len(text) - 1):
                            newText += line

                        else:
                            newText += line + '\n'
                
                    imageDraw.text((95 + 125 * column , 40 + 200 * row + 50 + 100 * x), newText, anchor="mm", font = ImageFont.truetype('roboto.ttf', 11), fill = (0, 0, 0))

    #)
    
    image.save(saveName)