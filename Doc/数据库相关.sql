
drop table Picture;
drop table Article;

/*
创建文章表
*/
create table Article(
    ID int not null auto_increment
    ,Title nvarchar(100) not null
    ,Content nvarchar(2000)
    ,CreateDate datetime
    ,SrcURL varchar(2000)
    ,IsDel bool default False
    ,ReadTime int default 0
    ,Type int default 0 -- 栏目分类 0 动画；1 电影 2 漫画
    ,constraint pk_article_id primary key(ID)
)charset utf8;

/*
创建图片表
*/
create table Picture(
    ID int not null auto_increment
    ,ArticleId int
    ,Name nvarchar(100)
    ,Path nvarchar(500) not null
    ,OrderNo int
    ,IsDel bool  default False
    ,Type int default 1   -- 0 封面；1 文章贴图
    ,SrcURL varchar(2000)
    ,constraint pk_picture_id primary key(ID)
    ,foreign key(ArticleId) references Article(ID)
)charset utf8;