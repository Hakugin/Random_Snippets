class MyGrid(wx.grid.Grid):
    """ A Copy&Paste enabled grid class"""
  # Original code found at:
  # https://stackoverflow.com/questions/28509629/work-with-ctrl-c-and-ctrl-v-to-copy-and-paste-into-a-wx-grid-in-wxpython
    def __init__(self, parent, id, style):
        wx.grid.Grid.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize, style)
        # wx.EVT_KEY_DOWN(self, self.OnKey)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKey)
        self.data4undo = [0, 0, '']
        self.dataRows = 0

    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            self.copy()
        # If Ctrl+V is pressed...
        if event.ControlDown() and event.GetKeyCode() == 86:
            self.paste('clip')
        # If Ctrl+Z is pressed...
        if event.ControlDown() and event.GetKeyCode() == 90:
            if self.data4undo[2] != '':
                self.paste('undo')
        # If del is pressed...
        if event.GetKeyCode() == 127:
            # Call delete method
            self.delete()
        # Skip other Key events
        if event.GetKeyCode():
            event.Skip()
            return

    def copy(self):
        # Number of rows and cols
        topleft = self.GetSelectionBlockTopLeft()
        if list(topleft) == []:
            topleft = []
        else:
            topleft = list(topleft[0])
        bottomright = self.GetSelectionBlockBottomRight()
        if list(bottomright) == []:
            bottomright = []
        else:
            bottomright = list(bottomright[0])
        if list(self.GetSelectionBlockTopLeft()) == []:
            rows = 1
            cols = 1
            iscell = True
        else:
            rows = bottomright[0] - topleft[0] + 1
            cols = bottomright[1] - topleft[1] + 1
            iscell = False
        # data variable contain text that must be set in the clipboard
        data = ''
        # For each cell in selected range append the cell value in the data variable
        # Tabs '    ' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                if iscell:
                    data += str(self.GetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c))
                else:
                    data += str(self.GetCellValue(topleft[0] + r, topleft[1] + c))
                if c < cols - 1:
                    data += '    '
            data += '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")

    def paste(self, stage):
      # This does not automatically add Rows
      # Maybe compare len(data.splitlines()) to grid.GetNumberRows()
      # Then append rows or maybe destroy and create the grid again?
      # - AppendRows()
        topleft = list(self.GetSelectionBlockTopLeft())
        if stage == 'clip':
            clipboard = wx.TextDataObject()
            if wx.TheClipboard.Open():
                wx.TheClipboard.GetData(clipboard)
                wx.TheClipboard.Close()
            else:
                wx.MessageBox("Can't open the clipboard", "Error")
            data = clipboard.GetText()
            if topleft == []:
                rowstart = self.GetGridCursorRow()
                colstart = self.GetGridCursorCol()
            else:
                rowstart = topleft[0][0]
                colstart = topleft[0][1]
            if (len(data.splitlines()) + self.dataRows) > self.GetNumberRows():
                self.dataRows += (len(data.splitlines()))
                self.AppendRows(self.dataRows - self.GetNumberRows() + 1)
                    
        elif stage == 'undo':
            data = self.data4undo[2]
            rowstart = self.data4undo[0]
            colstart = self.data4undo[1]
        else:
            wx.MessageBox("Paste method "+stage+" does not exist", "Error")
        text4undo = ''
        # Convert text in a array of lines
        for y, r in enumerate(data.splitlines()):
            # Convert c in a array of text separated by tab
            for x, c in enumerate(r.split('\t')): #modified to use the tab character
                if y + rowstart < self.NumberRows and x + colstart < self.NumberCols :
                    text4undo += str(self.GetCellValue(rowstart + y, colstart + x)) + '    '
                    self.SetCellValue(rowstart + y, colstart + x, c)
            text4undo = text4undo[:-1] + '\n'
        if stage == 'clip':
            self.data4undo = [rowstart, colstart, text4undo]
        else:
            self.data4undo = [0, 0, '']

        self.Parent.Refresh()

    def delete(self):
        # print "Delete method"
        # Number of rows and cols
        topleft = list(self.GetSelectionBlockTopLeft())
        bottomright = list(self.GetSelectionBlockBottomRight())
        if topleft == []:
            rows = 1
            cols = 1
        else:
            rows = bottomright[0][0] - topleft[0][0] + 1
            cols = bottomright[0][1] - topleft[0][1] + 1
        # Clear cells contents
        for r in range(rows):
            for c in range(cols):
                if topleft == []:
                    self.SetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c, '')
                else:
                    self.SetCellValue(topleft[0][0] + r, topleft[0][1] + c, '')
