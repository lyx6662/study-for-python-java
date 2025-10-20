const mysql2 = require('mysql2');
const pool = mysql2.createPool({
    host: 'localhost',
    user:'root',
    password:'Wadwad2020a',
    database:'lianyuan_database',
    port:3306,
    connectionLimit:10,
    queueLimit:0,
     waitForConnections: true
});
const db =pool.promise();
module.exports = db;