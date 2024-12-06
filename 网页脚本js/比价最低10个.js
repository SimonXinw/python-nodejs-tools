clearInterval(xwTimer);



// 定时器函数
const xwTimer = setInterval(() => {
  // 获取所有目标 <li> 元素
  const items = document.querySelectorAll(
    'li[data-testid="domains/search-item"]'
  );
  const buttonPrices = [];

  items.forEach((li) => {
    const button = li.querySelector("button");
    const priceSpan = button?.querySelector(".price");

    // 提取价格（去掉前缀 $ 和 ,，并转为数字），没有价格则跳过
    if (priceSpan) {
      const priceText = priceSpan.textContent
        .replace("$", "")
        .replace(/,/g, ""); // 去掉 $ 和 ,
      const priceValue = parseFloat(priceText); // 转为数字
      if (!isNaN(priceValue)) {
        buttonPrices.push({ button, price: priceValue });
      }
    }
  });

  // 按价格排序并取出最低的10个
  const sortedPrices = buttonPrices.sort((a, b) => a.price - b.price);
  const top10 = sortedPrices.slice(0, 5);

  // 更新样式
  buttonPrices.forEach(({ button }) => {
    if (top10.some((item) => item.button === button)) {
      // 最低价格的10个字体变红
      button.style.color = "red";
    } else {
      // 不是最低的10个恢复默认颜色
      button.style.color = "rgb(0, 112, 243)";
    }
  });
}, 3); // 每5秒执行一次
