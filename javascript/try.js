function tries() {
  var s = [2, 4, 44];
  var d = {
    e: function(){
      return 2;
    }
  }

  var that = {
    m: 5,
    x: 200,
    c: function(p){
      that.price = p;
      return p + d.e() + that.m;
    }
  }

  that.b = function (price) {
    return price*10;
  }

  return that;
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
