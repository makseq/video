function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie = c_name + "=" + c_value;
}

function getCookie(c_name) {
    var c_value = document.cookie;
    var c_start = c_value.indexOf(" " + c_name + "=");
    if (c_start == -1) {
        c_start = c_value.indexOf(c_name + "=");
    }
    if (c_start == -1) {
        c_value = null;
    } else {
        c_start = c_value.indexOf("=", c_start) + 1;
        var c_end = c_value.indexOf(";", c_start);
        if (c_end == -1) {
            c_end = c_value.length;
        }
        c_value = unescape(c_value.substring(c_start, c_end));
    }
    return c_value;
}

function saveValue(input, value) {
    var name = input.attr('id');
    setCookie(name, value, 365);
}

function getValue(input) {
    var name = input.attr('id');
    var value = getCookie(name);
    
    if(value != null && value != "" && typeof value != "undefined") {
        return value;
    }
    else {
        return null;
    }
}

$('.title').each(function(){
    var value = getValue($(this));
    if (value!=null)
        $(this).css('background-color', value);
}).on('blur', function(){
    if($(this).css('background-color') != '') {
        saveValue($(this), input.css('background-color'));
    }
});