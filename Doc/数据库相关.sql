/*
创建文章表
*/
create table Article(
    ID int not null auto_increment
    ,Title nvarchar(100) not null
    ,Content nvarchar(2000)
    ,CreateDate datetime
    ,IsSel bool
    ,ReadTime int
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
    ,IsDel bool
    ,constraint pk_picture_id primary key(ID)
    ,foreign key(ArticleId) references Article(ID)
)charset utf8;