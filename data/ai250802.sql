/*
 Navicat Premium Data Transfer

 Source Server         : ai2508
 Source Server Type    : MySQL
 Source Server Version : 80020
 Source Host           : localhost:3306
 Source Schema         : ai250802

 Target Server Type    : MySQL
 Target Server Version : 80020
 File Encoding         : 65001

 Date: 12/12/2025 15:18:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `uid` int(0) NOT NULL AUTO_INCREMENT COMMENT '用户编号',
  `uname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '用户名',
  `upwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '密码',
  `createtime` datetime(0) DEFAULT NULL COMMENT '账号创建时间',
  `imgpath` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '用户头像地址',
  `ustate` int(0) DEFAULT NULL COMMENT '用户状态\r\n用户状态 1：在用  0：删除',
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '张三', '123456', '2025-11-15 22:54:01', 'path/img.jpg', 1);
INSERT INTO `users` VALUES (2, 'lisi', '123123', '2025-11-15 23:03:21', 'imgpath', 1);
INSERT INTO `users` VALUES (13, 'lyz', '3b35a717c62a2bad4263d916074fc777', '2025-12-10 11:14:22', 'img/img.jpg', 1);
INSERT INTO `users` VALUES (14, 'lyz', '4297f44b13955235245b2497399d7a93', '2025-12-10 11:36:49', 'img/img.jpg', 1);

-- ----------------------------
-- Table structure for videos
-- ----------------------------
DROP TABLE IF EXISTS `videos`;
CREATE TABLE `videos`  (
  `video_id` int(0) NOT NULL COMMENT '视频id',
  `uid` int(0) NOT NULL COMMENT '视频对应的用户id',
  `video_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频路径',
  `create_time` datetime(0) DEFAULT NULL COMMENT '创建时间',
  `video_state` int(0) DEFAULT NULL COMMENT '视频状态显示 1显示 0隐藏',
  PRIMARY KEY (`video_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
