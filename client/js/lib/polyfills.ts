type Predicate<T> = (o: T) => boolean;

interface Array<T> {
  remove(item: T): Array<T>;
  findIndex(item: Predicate<T>): number;
}

Array.prototype.remove || (Array.prototype.remove = function (item) {
  var index = this.indexOf(item);
  if (index >= 0) {
    this.splice(index, 1);
  }
  return item;
});

Array.prototype.findIndex || (Array.prototype.findIndex = function(predicate: (item: any) => boolean): number {
  if (this === null) {
    throw new TypeError('Array.prototype.findIndex called on null or undefined');
  }
  if (typeof predicate !== 'function') {
    throw new TypeError('predicate must be a function');
  }
  const thisArg = arguments[1];
  let value: any;

  for (var i = 0; i < this.length; i++) {
    value = this[i];
    if (predicate.call(thisArg, value, i, this)) {
      return i;
    }
  }
  return -1;
});
