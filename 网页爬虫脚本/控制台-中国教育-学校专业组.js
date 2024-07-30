(async function () {
    /**
     * @爬取的网页 https://www.gaokao.cn/school/108/provinceline
    */
    function waitForElementUpdate(targetEle, afterListenFn, timeout = 5000,) {
        return new Promise((resolve, reject) => {
            let timer;
            let observer;

            const timeoutHandler = () => {
                observer.disconnect();
                reject(new Error('Error：等待更新超时！'));
            };

            const observerHandler = (mutationsList) => {
                for (const mutation of mutationsList) {
                    if (mutation.type === 'childList' || mutation.type === 'attributes') {
                        clearTimeout(timer);
                        observer.disconnect();
                        resolve(false);
                        return;
                    }
                }
            };

            timer = setTimeout(timeoutHandler, timeout);

            observer = new MutationObserver(observerHandler);

            observer.observe(targetEle, { attributes: true, childList: true, subtree: true });

            afterListenFn?.()
        });
    }


    function transformData(data, schoolName) {
        const header = data[0];

        const result = [["院校名称", "专业组", "选科", "包含专业"]];

        const groupMap = {};

        for (let i = 1; i < data.length; i++) {
            const row = data[i];

            const group = row[header.indexOf("专业组")];
            const major = row[header.indexOf("专业名称")] + '-' + row[header.indexOf("计划招生")];;
            const subject = row[header.indexOf("选科要求")];

            if (!groupMap[group]) {
                groupMap[group] = {
                    group: group,
                    subject: subject,
                    majors: []
                };
            }

            groupMap[group].majors.push(major);
        }

        for (let key in groupMap) {
            result.push([
                schoolName,
                groupMap[key].group,
                groupMap[key].subject,
                groupMap[key].majors.join(", ")
            ]);
        }

        return result;
    }

    function extractData(tableElement, groupName) {

        if (!tableElement) return [];

        const data = [];

        const rows = Array.from(tableElement.querySelectorAll('tr'));

        for (const row of rows) {
            const columns = Array.from(row.querySelectorAll('td'));

            data.push([
                columns[0]?.innerText,
                columns[1]?.innerText,
                columns[2]?.innerText,
                columns[3]?.innerText,
                columns[4]?.innerText,
                groupName
            ]);
        }

        return data
    }


    function waitTime(time = 1000) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve();
            }, time);
        });
    }

    const schoolName = document.querySelector('.school-tab_name__3pOZK')?.innerText;

    const containerEle = document.querySelector('.layoutWrap.clearfix')

    const scoreTabEle = document.querySelectorAll('.school-tab_tabNavs__1wdWg .school-tab_item__3J3Fh')[1]

    try {
        // 等待 - 省份加载完成
        await waitForElementUpdate(containerEle, () => {
            // 先监听，在点击
            scoreTabEle.click();
        }, 2000);
    } catch (error) {
        console.error('Error: 点击分数计划监听变化失败', error.message);
    }

    await waitTime(1000);

    // 1.找到 id="zs_plan" 父元素
    const zsPlanElement = document.getElementById('zs_plan');

    const selectsParentEle = zsPlanElement.querySelector('.slt-drop.flex-fsx')

    const proviceSelectEle = selectsParentEle.querySelectorAll('.ant-select.ant-select-enabled')?.[0];


    try {
        // 等待 - 省份加载完成
        await waitForElementUpdate(selectsParentEle, () => {
            // 先监听，在点击
            proviceSelectEle.click();
        }, 1000);
    } catch (error) {
        console.error('Error: 点击父元素失败', error.message);
    }

    console.log('选择框 bar, 等待省份是否全部加载', selectsParentEle)

    const proviceOptionWrapEles = selectsParentEle.children[5];

    const proviceOptionEles = proviceOptionWrapEles.querySelectorAll('ul li')

    Array.from(proviceOptionEles).forEach(async proviceOptionEle => {

        if (proviceOptionEle.innerText === '江西') {

            try {
                // 等待 - 全部专业组加载完成
                await waitForElementUpdate(selectsParentEle, () => {
                    // 先监听，在点击
                    proviceOptionEle.click();
                }, 1000);
            } catch (error) {
                console.error('Error: 点击父元素失败', error.message);
            }

        }

    });



    // 2.找到子元素 <div class="ant-select-selection-selected-value" title="全部专业组" style="display: block; opacity: 1;">全部专业组</div> 进行点击
    const allGroupsElement = zsPlanElement.querySelector('div.ant-select-selection-selected-value[title="全部专业组"]');

    allGroupsElement.click();

    // 3. 等待
    await new Promise(resolve => setTimeout(resolve, 800)); // 等待1秒

    // 4.找到 id="zs_plan" 父元素下面的这个全部专业组元素
    const zsPlanElement1 = document.getElementById('zs_plan');

    console.log('zs_plan >>>>>', zsPlanElement1)

    // 查找所有具有指定 class 名的 <li> 元素
    const allGroupsOptionsElements = document.querySelectorAll('li.ant-select-dropdown-menu-item.ant-select-dropdown-menu-item-active');

    // 遍历这些元素，找到包含特定文本内容的元素
    let allGroupsOptionElement;

    allGroupsOptionsElements.forEach(element => {
        if (element.innerText === '全部专业组') {
            allGroupsOptionElement = element;
        }
    });

    // console.log('选择框元素 >>>>>', allGroupsOptionElement)

    const selectParentDom = allGroupsOptionElement.parentElement;

    // 5.遍历 selectParentDom 元素下面的所有 <li> 子元素
    const optionElements = Array.from(selectParentDom.querySelectorAll('li.ant-select-dropdown-menu-item'));

    // console.log('选择框子元素 >>>>>', optionElements)

    // 6.避开 selectParentDom 元素下面的第一个全部专业组元素，开始依次点击从第二个开始的所有元素，注意记录下点击顺序
    let data = [];

    // 过滤第一个全部专业组选项，不点击
    const majorsOptionEles = Array.from(optionElements).slice(1);

    for (const optionElement of majorsOptionEles) {

        // console.log('专业选择 dom>>>>>>>>', optionElement)

        // 7.每一次点击之后等待表格重新加载完成，抓取里面的数据
        const tableElement = document.querySelector('#zs_plan .province_score_line_table table tbody');

        try {
            // 等待表格重新加载完成
            await waitForElementUpdate(tableElement, () => {
                // 先监听，在点击
                optionElement.click();
            }, 1800);
        } catch (error) {
            console.error(error.message);
        }

        // 7.每一次点击之后等待表格重新加载完成，抓取里面的数据
        const paginationItemEles = document.querySelectorAll('#zs_plan .pagination_box ul li');

        console.log('分页父级 dom>>>>>>>>', paginationItemEles)

        const paginationItemElesArr = Array.from(paginationItemEles)


        if (paginationItemElesArr?.length > 0) {
            const pageSize = Number(paginationItemElesArr[paginationItemElesArr.length - 2].querySelector('a').innerText)

            const nextBtnEle = paginationItemElesArr[paginationItemElesArr.length - 1].querySelector('span')

            console.log('分页数 dom>>>>>>>>', pageSize, '按钮', nextBtnEle)

            for (let i = 0; i < pageSize; i++) {
                // 7.每一次点击之后等待表格重新加载完成，抓取里面的数据
                const tableElement = document.querySelector('#zs_plan .province_score_line_table table tbody');

                data = data.concat(extractData(tableElement, optionElement.innerText));

                console.log('第 ' + i + ' 页  抓取的数据>>>>>>>>', data)

                try {
                    // 等待表格重新加载完成
                    await waitForElementUpdate(tableElement, () => {
                        // 先监听，在点击
                        nextBtnEle.click();
                    }, 1600);
                } catch (error) {
                    console.error('分页失败', error.message);
                }

            }

            continue;

        } else {
            // 直接抓取
            data = data.concat(extractData(tableElement, optionElement.innerText));
        }

    }

    const oldData = [
        ['专业名称', '计划招生', '学制', '学费', '选科要求', '专业组'], // 表头
        ...data // 数据
    ]

    console.log('抓取的原始数据 >>>>>', oldData)
    console.log('学校名字 >>>>>', schoolName)

    const formatData = transformData(oldData, schoolName);

    console.log('格式化后的数据 >>>>>', formatData)

    // 2. 引入SheetJS库
    const script = document.createElement('script');

    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js';

    script.onload = () => {
        // 3. 数据转化为Excel文件
        const ws = XLSX.utils.aoa_to_sheet(formatData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

        // 4. 下载Excel文件
        XLSX.writeFile(wb, '院校招生专业组专业明细.xlsx');
    };
    document.head.appendChild(script);
})();
