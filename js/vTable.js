Vue.component('v-table', {
    props: {
        //表头列名称
        columns: {
            type: Array,
            default: function () {
                return [];
            }
        },
        //数据
        data: {
            type: Array,
            default: function () {
                return [];
            }
        },
        // 分页
        page: {
            type: Number,
            default: function () {
                return 10;
            }
        },
        pageid: {
            type: Number,
            default: function () {
                return 0
            }
        }
    },
    //为了不影响原始数据，这里定义了相应的需要操作的数据对象
    data: function () {
        return {
            currentColumns: [],
            currentData: [],
            tmpData: [],
        }
    },
    //render 实现方式
    render: function (createElement) {
        let that = this;

        /**
         * 创建列样式与表头
         */
        let ths = [];//<th> 标签数组
        let cols = [];//<cols> 标签数组
        this.currentColumns.forEach(function (col, index) {
            if (col.width) {//创建列样式
                cols.push(createElement('col', {
                    style: {
                        width: col.width
                    }
                }))
            }

            if (col.sortable) {
                ths.push(createElement('th', [
                    createElement('span', col.title),
                    //升序
                    createElement('a', {
                        class: {
                            on: col.sortType === 'asc'
                        },
                        on: {
                            click: function () {
                                that.sortByAsc(index)
                            }
                        }
                    }, '↑'),
                    //降序
                    createElement('a', {
                        class: {
                            on: col.sortType === 'desc'
                        },
                        on: {
                            click: function () {
                                that.sortByDesc(index);
                            }
                        }
                    }, '↓')
                ]));
            } else {
                ths.push(createElement('th', col.title));
            }
        });


        /**
         * 创建内容
         */
        let trs = [];//<tr> 标签数组
        this.currentData.forEach(function (row) {//遍历行
            let tds = [];//<td> 标签数组
            that.currentColumns.forEach(function (cell) {//遍历单元格
                tds.push(createElement('td', row[cell.key]));
            });
            trs.push(createElement('tr', tds));
        });

        return createElement('table', [
            createElement('colgroup', cols),
            createElement('thead', [
                createElement('tr', ths)
            ]),
            createElement('tbody', trs)
        ])
    },

    methods: {
        //初始化表头
        initColumns: function () {
            this.currentColumns = this.columns.map(function (col, index) {
                //新建字段，标识当前列排序类型；默认为“不排序”
                col.sortType = 'normal';
                //新建字段，标识当前列在数组中的索引
                col.index = index;
                return col;
            });
        },
        //初始化数据
        initData: function () {
            // this.currentData = this.data.map(function (row, index) {
            this.tmpData = this.data.map(function (row, index) {
                //新建字段，标识当前行在数组中的索引
                row.index = index;
                return row;
            });
            let pageid = this.pageid;
            let page = this.page;
            this.currentData = this.tmpData.slice(pageid*page, (pageid+1) * page);
        },

        //排序
        order: function (index, type) {
            this.currentColumns.forEach(function (col) {
                col.sortType = 'normal';
            });

            //设置排序类型
            this.currentColumns[index].sortType = type;

            //设置排序函数
            let sortFunction;
            let key = this.currentColumns[index].key;
            switch (type) {
                default://默认为 asc 排序
                case 'asc':
                    sortFunction = function (a, b) {
                        return a[key] > b[key] ? 1 : -1;
                    };
                    break;
                case 'desc':
                    sortFunction = function (a, b) {
                        return a[key] < b[key] ? 1 : -1;
                    };
                    break;
            }
            this.currentData.sort(sortFunction);
        },

        //升序
        sortByAsc: function (index) {
            this.order(index, 'asc');
        },
        //降序
        sortByDesc: function (index) {
            this.order(index, 'desc');
        },
    },
    watch: {
        pageid: function(){
            // 变换展示条目数量时
            let pageid = this.pageid;
            let page = this.page;
            this.currentData = this.tmpData.slice(pageid*page, (pageid+1) * page);
        },
        page: function(){
            // 变换展示条目数量时
            let pageid = this.pageid;
            let page = this.page;
            this.currentData = this.tmpData.slice(pageid*page, (pageid+1) * page);
        },
        columns: function(){
          this.initColumns();
        },
        data: function () {
            this.initData();

            //找出排序字段
            let sortedColumn = this.currentColumns.filter(function (col) {
                return col.sortType !== 'normal';
            });

            if (sortedColumn.length > 0) {
                if (sortedColumn[0].sortType === 'asc') {
                    this.sortByAsc(sortedColumn[0].index);
                } else {
                    this.sortByDesc(sortedColumn[0].index);
                }
            }
        }
    },
    mounted() {
        this.initColumns();
        this.initData();
    }
});
