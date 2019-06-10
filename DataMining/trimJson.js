'use strict';

const fs = require('fs');

function trimObj(obj) {
  if (!Array.isArray(obj) && typeof obj != 'object') return obj;
  return Object.keys(obj).reduce(function(acc, key) {
    acc[key.trim()] = typeof obj[key] == 'string'? obj[key].trim() : trimObj(obj[key]);
    return acc;
  }, Array.isArray(obj)? []:{});
}

process.argv.forEach(function (val, index, array) {
  if(index > 1){
    console.log("trimming " + val);
    fs.readFile(val, (err, data) => {
      if (err) throw err;
      fs.writeFileSync('trim_' + val, JSON.stringify(trimObj(JSON.parse(data))));
      console.log('export as trim_' + val);
    });
  }
});

