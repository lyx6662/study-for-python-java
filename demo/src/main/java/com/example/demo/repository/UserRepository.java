package com.example.demo.repository;

import com.example.demo.model.User; // 导入你的实体类
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List; // 导入 List
/**
 * @Repository 注解将这个接口标记为 Spring 管理的数据仓库组件。
 */
@Repository
/**
 * 通过继承 JpaRepository，UserRepository 就自动拥有了大量的数据库操作方法，例如：
 * - findAll(): 查询所有记录
 * - findById(): 根据主键查询
 * - save(): 保存或更新记录
 * - delete(): 删除记录
 * ... 等等
 *
 * JpaRepository<User, Integer> 泛型参数说明：
 * - 第一个参数 (User): 指明这个 Repository 操作的是 User 实体类。
 * - 第二个参数 (Integer): 指明 User 实体类的主键 (userId) 的类型是 Integer。
 */
public interface UserRepository extends JpaRepository<User, Integer> {
    // 你现在不需要在这里写任何代码！
    // 如果未来有更复杂的查询需求，比如 "根据用户名查询用户"，可以在这里定义方法。
    List<User> findByUsername(String username);
}