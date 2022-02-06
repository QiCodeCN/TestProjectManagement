
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for request
-- ----------------------------
DROP TABLE IF EXISTS `request`;
CREATE TABLE `request` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(200) DEFAULT NULL COMMENT '提测标题',
  `appId` varchar(50) DEFAULT NULL COMMENT '应用服务',
  `developer` varchar(255) DEFAULT NULL COMMENT '提测RD',
  `tester` varchar(255) DEFAULT NULL COMMENT '测试QA',
  `CcMail` varchar(500) DEFAULT NULL COMMENT '关系人',
  `version` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '提测版本',
  `type` tinyint(1) DEFAULT NULL COMMENT '提测类型 1.功能 2.性能 3.安全',
  `scope` text COMMENT '测试说明',
  `gitCode` varchar(200) DEFAULT NULL COMMENT '项目代码',
  `wiki` varchar(200) DEFAULT NULL COMMENT '产品文档',
  `more` text COMMENT '是否发送邮件，0未操作，1成功，2失败',
  `status` tinyint(1) DEFAULT NULL COMMENT '测试状态 1-已提测 2-测试中 3-通过 4-失败 9-废弃',
  `sendEmail` tinyint(1) DEFAULT NULL COMMENT '是否发送消息，0未操作，1成功，2失败',
  `isDel` tinyint(1) DEFAULT '0' COMMENT '状态0正常1删除',
  `createUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '创建人',
  `createDate` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '修改人',
  `updateDate` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `test_desc` varchar(2000) DEFAULT '' COMMENT '结论描述',
  `test_risks` varchar(2000) DEFAULT '' COMMENT '风险提示',
  `test_cases` varchar(2000) DEFAULT '' COMMENT '测试用例描述',
  `test_bugs` varchar(1000) DEFAULT '' COMMENT '缺陷列表',
  `test_file` varchar(255) DEFAULT '' COMMENT '附件文件地址',
  `test_note` varchar(1000) DEFAULT '' COMMENT '报告备注',
  `test_email` tinyint(1) DEFAULT '0' COMMENT '是否发送消息，0未操作，1成功，2失败',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
