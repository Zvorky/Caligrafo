#! /usr/bin/python3

#	Caligrafo.py

''' Enzo Zavorski Delevatti
||| @Zvorky
\\\          ___,
 \\\      .~´    `-,
  \\°    /  _    _ \.
   \°   ,\`|_|''|_|´\
    °    /          /)   °
        (\  ,    , .\`   |°
         `) ;`,; `,^,)   ||°
         ´,´  `,  `  `   |||
                          \\\
        March     2023     |||
                           '''




import os



class Spacing:
    def __init__(self, paragraph = 4, left = 0, right = 0, top = 0, bottom = 0):
        self.paragraph = paragraph
        self.left   = left
        self.right  = right
        self.top    = top
        self.bottom = bottom
    

    def SetMargin(self, amount: int):
        if(amount < 0):
            return False
        self.left = self.right = self.top = self.bottom
        return True
    

    def CenterMargin(self):
        self.left = self.right = (self.left + self.right) / 2
        self.top = self.bottom = (self.top + self.bottom) / 2



class TextBox:
    def __init__(self, text = '', width = 0, height = 0):
        self.text = text
        self.width = width
        self.height = height
        self.spacing = Spacing()
        self.alignH = 'left'
        self.alignV = 'top'
    

    #   Horizontal Alignment = left; center; right; justified
    def SetAlignmentH(self, align: str):
        align = align.lower()
        if(align != 'left' and align != 'center' and align != 'right' and align != 'justified'):
            return False
        self.alignH = align
        return True
    

    #   Vertical Alignment = top; center; bottom
    def SetAlignmentV(self, align: str):
        align = align.lower()
        if(align != 'top' and align != 'center' and align != 'bottom'):
            return False
        self.alignV = align
        return True
    

    def SetMargin(self, amount: int):
        return self.spacing.SetMargin(amount)
    

    def CenterMargin(self):
        self.spacing.CenterMargin()
    

    #   Return the text with the formatting applied
    def ConvertStr(self):

        # get the right paragraph spacing
        if(self.width > 0 and self.spacing.paragraph >= self.width):
            paragraph = (self.width-1)
        else:
            paragraph = self.spacing.paragraph
        
        # starts with paragraph
        string = ' ' * paragraph

        # current indexes (column and line starts at 1)
        column = paragraph
        line   = 1
        i      = 0

        # shows when text exceeds the box size
        limit = '[...]'

        for char in self.text:
            
           # New Line
            if(char == '\n'):
                # Height Limit
                if(line == self.height):
                    string += ' ' * (self.width - column)
                    string = string[0:len(string)-len(limit)] + limit
                    return string
                
                # New Line into Paragraph
                string += '\n' + ' ' * paragraph
                column += paragraph
                line   += 1
            
            # Width Limit
            elif(column == self.width):
                string += '\n' + char
                line   += 1
                column  = 1
            
            else:
                string += char
                column += 1

            i += 1

        return string



test = TextBox('xdddddddddddddddddd\no.o')
test.width = 16
test.height = 2
print(test.ConvertStr())