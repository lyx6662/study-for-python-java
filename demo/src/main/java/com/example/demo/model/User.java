package com.example.demo.model;

import jakarta.persistence.*; // 导入JPA注解
import java.time.LocalDateTime; // 使用现代日期时间API

/**
 * @Entity 注解告诉 Spring Data JPA: 这是一个实体类，它将映射到数据库中的一个表。
 */
@Entity
/**
 * @Table(name = "users") 明确指定这个类映射到数据库中名为 "users" 的表。
 * 这是一个好习惯，可以避免因类名和表名不完全匹配（如大小写）而导致的问题。
 */
@Table(name = "users")
public class User {

    /**
     * @Id 标记这个字段是表的主键。
     */
    @Id
    /**
     * @Column(name = "user_id") 将 Java 属性 userId 映射到数据库的 user_id 列。
     * 如果Java属性名和数据库列名完全相同（忽略大小写），这个注解可以省略，但显式写上更清晰。
     */
    @Column(name = "user_id")
    private Integer userId; // 对应 SQL 中的 INT PRIMARY KEY

    private String username; // 自动映射到同名的 username 列
    private String account;
    private String password;
    private String email;
    private String address;
    private String phone;

    /**
     * 将 createTime 属性映射到 create_time 列。
     * Java中通常使用驼峰命名法(createTime)，而SQL中常用下划线(create_time)。
     */
    @Column(name = "create_time")
    private LocalDateTime createTime; // 对应 SQL 中的 DATETIME

    // --- JPA 要求实体类必须有 Getter 和 Setter 方法 ---

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getAccount() {
        return account;
    }

    public void setAccount(String account) {
        this.account = account;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public LocalDateTime getCreateTime() {
        return createTime;
    }

    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }
}