dataParse = {
  csvToArray: function (text) {
    /* takes in csv string and converts to an array*/
    var p = "",
      row = [""],
      ret = [row],
      i = 0,
      r = 0,
      s = !0,
      l;
    for (var li = 0; li < text.length; li++) {
      var l = text[li];
      if ('"' === l) {
        if (s && l === p) row[i] += l;
        s = !s;
      } else if ("," === l && s) l = row[++i] = "";
      else if ("\n" === l && s) {
        if ("\r" === p) row[i] = row[i].slice(0, -1);
        row = ret[++r] = [(l = "")];
        i = 0;
      } else row[i] += l;
      p = l;
    }
    return ret;
  },
  CSVTable: function (text) {
    /* takes in csv string and creates a csvTable oject*/
    var csvArr = dataParse.csvToArray(text);
    this.labels = csvArr[0];
    this.data = csvArr.slice(1, csvArr.length);
  },
};
