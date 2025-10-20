const express = require('express');//引入Express框架
const cors = require('cors');//引入跨域资源共享中间件
const db = require('./db');//引入数据库模块
const app = express();//将app作为Express应用实例
const port = 8082;


app.use(cors());
app.get('/api/users', async (req, res)=>{
    try{
        const [rows, fields] = await db.query('SELECT * FROM users');
        res.json(rows);
    }catch(err){
        console.error(err);
        res.status(500).json({error: '数据库查询失败'});
    }
});
    



app.get('/', (req,res)=>{
    res.send('Hello World!');
});




app.listen(port, ()=>{
    console.log(`在端口: ${port} 启动`);
});