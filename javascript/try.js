var tries = {
  s: [2, 4, 44],
  a: function () {
    var m = 5;
    var that = {};
    that.x = 200;
    that.c = function(p){
      that.price = p;
      return p + that.x + m;
    }
    return that;
  },
  b: function (price) {
    return price*10;
  },
  d: {
    e: function(){
      return 2;
    }
  }
}

var MYAPPLICATION = {
    calculateVat: function (base) {
        return base * 1.21;
    },
    product: function (price) {
        this.price = price;
        this.getPrice = function(){
                          return this.price;
                       };
    },
    doCalculations: function () {
        var p = new MYAPPLICATION.product(100);
        alert(this.calculateVat(p.getPrice()));
    }
}
