async function subscribeEmail(email) {
  if (!email || !email.includes("@")) {
    throw new Error("Invalid email address");
  }

  const KLAVIYO_LIST_ID = "R2zJFm";

  const KLAVIYO_API_KEY = "pk_2df33f4ed5e852d0e810530959a976de15";

  try {
    const response = await fetch(
      `https://a.klaviyo.com /api/lists/${KLAVIYO_LIST_ID}/relationships/profiles`,
      {
        method: "POST",
        headers: {
          accept: "application/vnd.api+json",
          revision: "2024-10-15",
          "content-type": "application/vnd.api+json",
          Authorization: `Klaviyo-API-Key ${KLAVIYO_API_KEY}`,
        },
        body: JSON.stringify({
          data: {
            type: "profile",
            attributes: {
              email: "simon.xinw@gmail.com",
            },
          },
        }),
      }
    );

    // 解析响应数据
    const responseData = await response.json();
    console.log("请求响应数据 >>>>>>>>>>>", responseData);

    if (response.ok) {
      return { message: "请求成功!", data: responseData };
    } else {
      // 如果响应不正常，获取错误信息
      throw new Error("请求失败: " + JSON.stringify(responseData));
    }
  } catch (error) {
    throw new Error("请求失败: " + error.message);
  }
}

const email = "simon.xinw@gmail.com";

subscribeEmail(email);
