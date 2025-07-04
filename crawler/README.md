|Info|Link||
|---|---|---|
|herolist|<https://pvp.qq.com/web201605/js/herolist.json>|https://pvp.qq.com/web201605/herodetail/+（ename）+.shtml|https://pvp.qq.com/web201605/herodetail/+（ename）+.shtml|
|item|<https://pvp.qq.com/web201605/js/item.json>|
|summoner|<https://pvp.qq.com/web201605/js/summoner.json>|
|ming|<https://pvp.qq.com/web201605/js/ming.json>|

## herolist.json
|参数名称|类型|参数描述|
|---|---|---|
|[]|list|英雄列表|
|ename|int|id|
|cname|str|中文名称|
|title|str|皮肤名称|
|pay_type|int|支付类型|
|new_type|int|新类型（）|
|hero_type|int|英雄主类型（坦克，法师）|
|hero_type2|Int|第二类型（辅助，坦克）|
|skin_name|str|准备属性表述|

|createHeroList({“data”:|list|英雄列表|
|---|---|---|
|heroid|int|id|
|title|str|中文名称|
|infourl|str|详细网页|
|camptype|int|支付类型|
|appointHeroid|int|App的英雄id|
|removeHeroid|int|删除的英雄id|
|occupation|Int|类型|
|num|str|排序|
|heroimg|str|英雄图片|
|faceimg|str|英雄头像|
|pinyin|Str|拼音|
