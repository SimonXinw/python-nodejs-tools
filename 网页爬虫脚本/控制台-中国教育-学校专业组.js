(async function () {

    const schoolName = document.querySelector('school-tab_name__3pOZK');

    // 1.找到 id="zs_plan" 父元素
    const zsPlanElement = document.getElementById('zs_plan');

    // 2.找到子元素 <div class="ant-select-selection-selected-value" title="全部专业组" style="display: block; opacity: 1;">全部专业组</div> 进行点击
    const allGroupsElement = zsPlanElement.querySelector('div.ant-select-selection-selected-value[title="全部专业组"]');
    allGroupsElement.click();

    // 3. 等待
    await new Promise(resolve => setTimeout(resolve, 1000)); // 等待1秒

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

    console.log('选择框元素 >>>>>', allGroupsOptionElement)

    const selectParentDom = allGroupsOptionElement.parentElement;

    // 5.遍历 selectParentDom 元素下面的所有 <li> 子元素
    const optionElements = Array.from(selectParentDom.querySelectorAll('li.ant-select-dropdown-menu-item'));

    console.log('选择框子元素 >>>>>', optionElements)

    // 6.避开 selectParentDom 元素下面的第一个全部专业组元素，开始依次点击从第二个开始的所有元素，注意记录下点击顺序
    const data = [];
    for (let i = 1; i < optionElements.length; i++) {
        const optionElement = optionElements[i];
        optionElement.click();

        // 7.每一次点击之后等待表格重新加载完成，抓取里面的数据
        await new Promise(resolve => setTimeout(resolve, 1000)); // 等待2秒，确保表格加载完成

        const tableElement = document.querySelector('#zs_plan .province_score_line_table table tbody');

        if (tableElement) {
            const rows = Array.from(tableElement.querySelectorAll('tr'));

            rows.forEach(row => {
                const columns = Array.from(row.querySelectorAll('td'));
                data.push([
                    columns[0]?.innerText,
                    columns[1]?.innerText,
                    columns[2]?.innerText,
                    columns[3]?.innerText,
                    columns[4]?.innerText,
                    optionElements[i].innerText // 记录点击的专业组名称
                ]);
            });
        }
    }

    function transformData(data) {
        const header = data[0];
        const result = [["院校名称", "专业组", "选科", "包含专业"]];

        const groupMap = {};

        for (let i = 1; i < data.length; i++) {
            const row = data[i];
            const group = row[header.indexOf("专业组")];
            const major = row[header.indexOf("专业名称")];
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



    const oldData = [
        ['专业名称', '计划招生', '学制', '学费', '选科要求', '专业组'], // 表头
        ...data // 数据
    ]

    console.log('抓取的原始数据 >>>>>', oldData)

    const formatData = transformData(oldData);

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
