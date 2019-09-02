/*
Navicat MySQL Data Transfer

Source Server         : 123.207.243.40
Source Server Version : 50725
Source Host           : 123.207.243.40:3306
Source Database       : money

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-09-02 11:44:48
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for code
-- ----------------------------
DROP TABLE IF EXISTS `code`;
CREATE TABLE `code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL COMMENT '名称',
  `symbol` varchar(64) DEFAULT NULL COMMENT '代码',
  `turnover_rate` decimal(11,2) DEFAULT NULL COMMENT '换手率',
  `concept` varchar(255) DEFAULT NULL COMMENT '概念',
  `northward_funds_days` int(11) DEFAULT NULL COMMENT '北向资金流入天数',
  `northward_funds_detail` varchar(255) DEFAULT NULL COMMENT '北向资金详情',
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `short` varchar(255) DEFAULT NULL COMMENT '短期趋势',
  `medium` varchar(255) DEFAULT NULL COMMENT '中期趋势',
  `short_buy` varchar(255) DEFAULT NULL COMMENT '短期买入建议',
  `medium_buy` varchar(255) DEFAULT NULL COMMENT '中期买入建议',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15037 DEFAULT CHARSET=utf8 COMMENT='股票代码';

-- ----------------------------
-- Table structure for one_night_stand
-- ----------------------------
DROP TABLE IF EXISTS `one_night_stand`;
CREATE TABLE `one_night_stand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '名称',
  `symbol` varchar(255) DEFAULT NULL COMMENT '代码',
  `type` varchar(255) DEFAULT NULL COMMENT '类型',
  `northward_funds_day` int(11) DEFAULT NULL COMMENT '北向资金增持天数',
  `northward_funds_detail` varchar(255) DEFAULT NULL COMMENT '北向资金详情',
  `concept` varchar(255) DEFAULT NULL COMMENT '概念',
  `price` decimal(10,2) DEFAULT NULL COMMENT '现价',
  `ma60` decimal(10,2) DEFAULT NULL COMMENT 'ma60',
  `percent_ma60` decimal(10,2) DEFAULT NULL COMMENT '现价相对ma60偏移',
  `ma20` decimal(10,2) DEFAULT NULL,
  `percent_ma20` decimal(10,2) DEFAULT NULL,
  `ma10` decimal(10,2) DEFAULT NULL,
  `percent_ma10` decimal(10,2) DEFAULT NULL,
  `ma5` decimal(10,2) DEFAULT NULL,
  `percent_ma5` decimal(10,2) DEFAULT NULL,
  `create_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=979 DEFAULT CHARSET=utf8;
