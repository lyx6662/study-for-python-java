package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * @Configuration 注解表明这是一个 Spring 配置类。
 */
@Configuration
public class WebConfig {

    /**
     * @Bean 注解将这个方法返回的对象注册为一个 Spring Bean。
     * Spring Boot 会自动检测到这个 Bean 并应用它。
     */
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            /**
             * 重写 addCorsMappings 方法来配置 CORS。
             * @param registry CORS 配置注册表
             */
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                // addMapping("/**") 表示对应用中的所有接口路径都应用这个 CORS 配置。
                registry.addMapping("/**")
                        // allowedOrigins(...) 指定了允许发起跨域请求的来源。
                        // 这里我们明确指定只允许你的前端应用 http://localhost:5173。
                        .allowedOrigins("http://localhost:5173")
                        // allowedMethods(...) 指定了允许的 HTTP 请求方法，如 GET, POST 等。
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        // allowedHeaders("*") 允许请求中携带任何头信息。
                        .allowedHeaders("*")
                        // allowCredentials(true) 表示允许服务器响应中包含凭证（如 cookies）。
                        .allowCredentials(true);
            }
        };
    }
}