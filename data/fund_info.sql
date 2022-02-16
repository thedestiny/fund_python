
CREATE DATABASE IF NOT EXISTS `fund_data` DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE `tb_fund_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(6) NOT NULL DEFAULT '' COMMENT '基金代码',
  `name` varchar(100) DEFAULT '' COMMENT '基金名称',
  `alias` varchar(255) DEFAULT NULL COMMENT '基金别名',
  `fund_type` varchar(2) DEFAULT NULL COMMENT '基金类型 0-HS300 1-股票基金 2-混合基金 3-ETF基金',
  `fund_size` decimal(10,3) DEFAULT '0.0' COMMENT '基金规模',
  `fund_manager` varchar(100) DEFAULT '' COMMENT '基金经理',
  `fund_company` varchar(100) DEFAULT '' COMMENT '基金公司',
  `create_time` int(100) NOT NULL DEFAULT '' COMMENT '成立日期',
  `update_time` int(100) NOT NULL DEFAULT '' COMMENT '基金规模更新日期',
  `format_time` int(100) NOT NULL DEFAULT '' COMMENT '净值更新日期',
  `comp_basic` varchar(1000)  DEFAULT '' COMMENT '业绩基准',
  `index_target` varchar(1000) DEFAULT '' COMMENT '跟踪标的',
  `price` decimal(8,4) DEFAULT '0.0000' COMMENT '基金价格',
  `price_change` decimal(8,4) DEFAULT '0.0000' COMMENT '价格变动',
  `rate_change` decimal(8,4) DEFAULT '0.0000' COMMENT '变动比例',
  `href` varchar(100) DEFAULT '0' COMMENT '访问链接',
  `etf_flag` varchar(1) DEFAULT '0' COMMENT 'ETF基金标记',
  `stage_week1` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近一周',
  `stage_month1` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近一个月',
  `stage_month3` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近三个月',
  `stage_month6` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近六个月',
  `stage_year` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-今年以来',
  `stage_year1` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近1年',
  `stage_year2` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近2年',
  `stage_year3` decimal(10,3) DEFAULT '0.000' COMMENT '阶段涨幅-近3年',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_fund_list_code` (`code`) USING BTREE,
  KEY `idx_fund_list_type` (`fund_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基金信息列表';


CREATE TABLE `tb_fund_ext_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(6) NOT NULL DEFAULT '0' COMMENT '基金代码',
  `data_type` varchar(2) DEFAULT '1' COMMENT '数据类型 1 季度数据 2 年度数据',
  `data_name` varchar(10) DEFAULT '' COMMENT '数据名称',
  `data_value` decimal(10,3) DEFAULT '0.000' COMMENT '数据值',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_fund_list_code` (`code`) USING BTREE,
  KEY `idx_fund_list_type` (`code`,`data_type`,`data_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基金扩展信息列表';


CREATE TABLE `tb_stock_list` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(6) NOT NULL DEFAULT '' COMMENT 'stock代码',
  `name` varchar(100) DEFAULT '' COMMENT 'stock名称',
  `price` decimal(10,2) DEFAULT NULL COMMENT '当前价格',
  `earnings` decimal(18,4) DEFAULT NULL COMMENT '季度收益',
  `pe` decimal(18,4) DEFAULT NULL COMMENT '市盈率',
  `pb` decimal(18,4) DEFAULT NULL COMMENT '市净率',
  `roe` decimal(18,4) DEFAULT NULL COMMENT '净资产收益率',
  `net_asset` decimal(18,4) DEFAULT NULL COMMENT '每股净资产',
  `operating` decimal(18,4) DEFAULT NULL COMMENT '营业收入',
  `operating_rate` decimal(18,4) DEFAULT NULL COMMENT '营业收入增长比率',
  `proceeds` decimal(18,4) DEFAULT NULL COMMENT '净利润',
  `proceeds_rate` decimal(18,4) DEFAULT NULL COMMENT '净利润增长率',
  `gross` decimal(18,4) DEFAULT NULL COMMENT '毛利率',
  `net_margin` decimal(18,4) DEFAULT NULL COMMENT '净利率',
  `debt_ratio` decimal(18,4) DEFAULT NULL COMMENT '负债率',
  `equity` decimal(18,4) DEFAULT NULL COMMENT '总股本',
  `total_value` decimal(18,4) DEFAULT NULL COMMENT '总市值',
  `floating` decimal(18,4) DEFAULT NULL COMMENT '流通股',
  `flow_value` decimal(18,4) DEFAULT NULL COMMENT '流通值',
  `und_value` decimal(18,4) DEFAULT NULL COMMENT '未分配利润',
  `ipo_time` varchar(20) DEFAULT NULL COMMENT '上市时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '抓取时间',
  `q_time` int(11) DEFAULT NULL COMMENT '季报 201806 18年2季报',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_stock_list_code` (`code`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=100000 DEFAULT CHARSET=utf8 COMMENT='stock 信息列表';

