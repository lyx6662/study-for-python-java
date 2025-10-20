import { useState , useEffect } from 'react'//useState用于加载实时状态,useEffect用于加载API数据,例如网络请求
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [users, setUsers] = useState([]);//定义一个状态变量users,初始值为空数组
useEffect(() => {
    const fetchUsers = async () => {
      // 使用 try...catch 来捕获可能发生的错误
      try {
        const response = await fetch('http://localhost:8088/api/users');
        const data = await response.json();
        setUsers(data);
      } catch (error) {
        // 如果 fetch 失败（比如后端没开），会在这里捕获到错误
        console.error("获取数据失败:", error);
      }
    };

    fetchUsers();
  }, []);

  console.log(users);//在控制台打印获取到的用户数据

  return (
    <>
      <div>
        <h1>用户列表</h1>

        <ul>
          {users.map(user => (
            <li key={user.user_id}>{user.username}{user.password}</li>
          ))}
        </ul>
      </div>
    </>
  )
}

export default App
