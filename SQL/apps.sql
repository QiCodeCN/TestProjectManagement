
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for apps
-- ----------------------------
DROP TABLE IF EXISTS `apps`;
CREATE TABLE `apps` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `appId` varchar(50) DEFAULT NULL COMMENT '应用服务ID',
  `productId` bigint DEFAULT NULL COMMENT '外键关联产品所属',
  `note` varchar(100) DEFAULT NULL COMMENT '应用描述',
  `tester` varchar(300) DEFAULT NULL COMMENT '测试负责人',
  `developer` varchar(300) DEFAULT NULL COMMENT '默认研发负责人',
  `producer` varchar(300) DEFAULT NULL COMMENT '默认产品经理',
  `CcEmail` varchar(500) DEFAULT NULL COMMENT '默认抄送邮件或组',
  `gitCode` varchar(200) DEFAULT NULL COMMENT '代码地址',
  `wiki` varchar(200) DEFAULT NULL COMMENT '项目说明地址',
  `more` text COMMENT '更多的信息',
  `status` tinyint(1) DEFAULT '0' COMMENT '提测状态：1-已提测 2-测试中 3-通过 4-失败 9-废弃',
  `isDel` tinyint(1) DEFAULT '0' COMMENT '状态0正常1删除',
  `createUser` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '创建人',
  `createDate` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateUser` varchar(20) DEFAULT NULL COMMENT '修改人',
  `updateDate` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `apps_id_uindex` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10020 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='应用管理';

SET FOREIGN_KEY_CHECKS = 1;
