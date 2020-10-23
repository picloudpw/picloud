function random_ID() {
    return '_' + Math.random().toString(36).substr(2, 9);
}

Date.prototype.toPrettyString = function () {
    let dd = this.getDate();
    let mm = this.getMonth() + 1;

    let date = [
        (dd > 9 ? '' : '0') + dd,
        (mm > 9 ? '' : '0') + mm,
        this.getFullYear(),
    ].join('-');
    let time = [
        this.getHours(),
        this.getMinutes(),
    ].join(':');
    return `${date}${time === '3:0' ? '' : ' ' + time}`;
};

Date.prototype.toYYYYMMDD = function () {

    let dd = this.getDate();
    let mm = this.getMonth() + 1;

    return [
        this.getFullYear(),
        (mm > 9 ? '' : '0') + mm,
        (dd > 9 ? '' : '0') + dd,
    ].join('-');
};

function push_state(dict) {
    let kvp = [];

    for (let i in Object.keys(dict)) {
        let key = Object.keys(dict)[i];
        let value = encodeURI(dict[key]);
        key = encodeURI(key);
        kvp.push([key, value].join('='));
    }

    let new_search = "?" + kvp.join('&');
    history.pushState(null, null, new_search);
}
