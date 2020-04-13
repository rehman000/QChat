 function csvToArray(text) {
    /* takes in csv string and converts to an array*/
    var p = '', row = [''], ret = [row], i = 0, r = 0, s = !0, l;
    for (var li = 0; li < text.length; li++) {
        var l = text[li];
        if ('"' === l) {
            if (s && l === p) row[i] += l;
            s = !s;
        } else if (',' === l && s) l = row[++i] = '';
        else if ('\n' === l && s) {
            if ('\r' === p) row[i] = row[i].slice(0, -1);
            row = ret[++r] = [l = '']; i = 0;
        } else row[i] += l;
        p = l;
    }
    return ret;
};

function csvToObject(text) {
    /* takes in csv string and converts to an oject*/
    var csvArr = csvToArray(text);
    return {
        labels: csvArr[0],
        data: csvArr.slice(1, csvArr.length)
    };
}
