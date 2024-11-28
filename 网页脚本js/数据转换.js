(function () {
  const data = [
    {
      categoryTitle: "Key Features",
      categoryChildren: [
        {
          paramTitle: "Brightness",
          paramChildren: [
            {
              type: "icon-text",
              icon: "https://cdn.shopify.com/s/files/1/0554/7445/4576/files/projectors_comparison_icon_1.svg?v=1726197475",
              text: "3500 Peak Lumens",
              visible: true,
            },
            {
              type: "icon-text",
              icon: "https://cdn.shopify.com/s/files/1/0554/7445/4576/files/projectors_comparison_icon_1.svg?v=1726197475",
              text: "3000 Peak Lumens",
              visible: true,
            },
            {
              type: "icon-text",
              icon: "https://cdn.shopify.com/s/files/1/0554/7445/4576/files/projectors_comparison_icon_1.svg?v=1726197475",
              text: "2600 Peak Lumens",
              visible: true,
            },
          ],
        },
        {
          paramTitle: "IP Control",
          paramChildren: [
            {
              type: "icon-text",
              icon: "https://cdn.shopify.com/s/files/1/0554/7445/4576/files/projectors_comparison_icon_10.svg?v=1726197475",
              text: "PJLink, Control 4, SAVANT and Crestron",
              visible: true,
            },
            {
              type: "icon-text",
              icon: "https://cdn.shopify.com/s/files/1/0554/7445/4576/files/projectors_comparison_icon_10.svg?v=1726197475",
              text: "PJLink, Control 4, SAVANT and Crestron",
              visible: true,
            },
            {
              type: "icon-text",
              icon: "https://cdn.shopify.com/s/files/1/0554/7445/4576/files/projectors_comparison_icon_10.svg?v=1726197475",
              text: "PJLink, Control 4, SAVANT and Crestron",
              visible: false,
            },
          ],
        },
      ],
    },
    {
      categoryTitle: "Audio & Noise",
      categoryChildren: [
        {
          paramTitle: "Noise",
          paramChildren: [
            {
              type: "text",
              text: "<=30dB",
              visible: true,
            },
            {
              type: "text",
              text: "<=27dB",
              visible: true,
            },
            {
              type: "text",
              text: "<=27dB",
              visible: true,
            },
          ],
        },
      ],
    },
    {
      categoryTitle: "Power",

      categoryChildren: [
        {
          paramTitle: "Power Consumption",
          paramChildren: [
            {
              type: "text",
              text: "320 W",
              visible: true,
            },
            {
              type: "text",
              text: "185 W",
              visible: true,
            },
            {
              type: "text",
              text: "175 W",
              visible: true,
            },
          ],
        },
      ],
    },
    {
      categoryTitle: "General",

      categoryChildren: [
        {
          paramTitle: "Weight",
          paramChildren: [
            {
              type: "text",
              text: "21 Ibs / 10.8 kg",
              visible: true,
            },
            {
              type: "text",
              text: "21 Ibs / 9.5 kg",
              visible: true,
            },
            {
              type: "text",
              text: "21 Ibs / 9.5 kg",
              visible: true,
            },
          ],
        },
        {
          paramTitle: "Packaged Dimensions",
          paramChildren: [
            {
              type: "text",
              text: "29.0*19.5*11.8 inches / 736*495*300 mm",
              visible: true,
            },
            {
              type: "text",
              text: "29.0*19.5*11.8 inches / 736*495*300 mm",
              visible: true,
            },
            {
              type: "text",
              text: "29.0*19.5*11.8 inches / 736*495*300 mm",
              visible: true,
            },
          ],
        },
        {
          paramTitle: "Packaged Weight",
          paramChildren: [
            {
              type: "text",
              text: "31.7 lbs / 14.4 kg",
              visible: true,
            },
            {
              type: "text",
              text: "28.9 lbs / 13.1 kg",
              visible: true,
            },
            {
              type: "text",
              text: "28.9 lbs / 13.1 kg",
              visible: true,
            },
          ],
        },
      ],
    },
    {
      categoryTitle: "Platform",

      categoryChildren: [
        {
          paramTitle: "Display Technology",
          paramChildren: [
            {
              type: "text",
              text: "Tl 0.47-inch ecd DMD",
              visible: true,
            },
            {
              type: "text",
              text: "Tl 0.47-inch ecd DMD",
              visible: true,
            },
            {
              type: "text",
              text: "Tl 0.47-inch ecd DMD",
              visible: true,
            },
          ],
        },
      ],
    },
  ];

  const translateData = (arr) => {
    const data = arr.map((category) => {
      return {
        ...category,
        categoryChildren: category.categoryChildren.map((param) => {
          return {
            ...param,
            paramChildren: param.paramChildren.map((item, index) => {
              let productName;
              switch (index) {
                case 0:
                  productName = "LTV-3500 Pro";
                  break;
                case 1:
                  productName = "LTV-3000 Pro";
                  break;
                case 2:
                  productName = "LTV-2500";
                  break;
              }
              return { ...item, productName };
            }),
          };
        }),
      };
    });

    return data;
  };

  const newData = translateData(data);

  console.log("newDta >>>>>>>>>>>", newData);
})();
