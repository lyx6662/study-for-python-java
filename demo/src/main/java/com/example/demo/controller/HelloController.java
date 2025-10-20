package com.example.demo.controller;

import com.example.demo.model.User; // 导入 User 实体类
import com.example.demo.repository.UserRepository; // 导入 UserRepository
import org.springframework.beans.factory.annotation.Autowired; // 导入 Autowired
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam; // 导入 @RequestParam
import org.springframework.web.servlet.view.RedirectView; // 导入 RedirectView (方法二需要)

import java.util.List; // 导入 List

@RestController
@RequestMapping("/api")
public class HelloController {

    /**
     * @Autowired: 这是 Spring 的核心功能之一，称为“依赖注入”。
     * Spring 框架会自动找到 UserRepository 的一个实例，并把它赋值给这个 userRepository 变量。
     * 你不需要自己去 new 一个 UserRepository()。
     */
    @Autowired
    private UserRepository userRepository;

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello, World from Spring Boot!";
    }

    @GetMapping("/users")
    public List<User> getUsers(@RequestParam(name = "username", required = false) String username) {

        // 判断 URL 中是否传入了 username 参数
        if (username != null && !username.isEmpty()) {
            // 如果传入了，就调用我们刚刚在 UserRepository 中定义的新方法
            return userRepository.findByUsername(username);
        } else {
            // 如果没有传入，就还像以前一样，查询所有用户
            return userRepository.findAll();
        }
    }



    /**
     * 通过QQ号获取QQ头像的接口。
     * 这是一个推荐的、高效的实现方式：重定向。
     *
     * @param qq 接收来自URL的参数，例如：/api/qq-avatar?qq=2703466790
     * @return 返回一个重定向指令，让浏览器直接去QQ服务器获取头像
     */
    @GetMapping("/qq-avatar") // 建议使用英文路径
    public RedirectView getQqAvatar(@RequestParam("qq") String qq) {
        // 1. 构建最终的QQ头像API地址
        String qqAvatarUrl = "http://q1.qlogo.cn/g?b=qq&nk=" + qq + "&s=100";

        // 2. 创建一个 RedirectView 对象，它会告诉Spring Boot执行302重定向
        return new RedirectView(qqAvatarUrl);
    }


}