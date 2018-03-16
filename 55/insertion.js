db.course.insert({
    code: "COMP4332",
    ctitle: "Big Data Mining and Management",
    credit: "3",
    prerequisite: [{ code: "COMP4211" }, { code: "COMP4331" }, { code: "ISOM3360" }],
    colist: [{ code: "RMBI4310" }],
    description: "This course will expose students to new and practical issues of real world mining and managing big data. Data mining and management is to effectively support storage, retrieval, and extracting implicit, previously unknown, and potentially useful knowledge from data. This course will place emphasis on two parts. The first part is big data issues such as mining and managing on distributed data, sampling on big data and using some cloud computing techniques on big data. The second part is applications of the techniques learnt on areas such as business intelligence, science and engineering, which aims to uncover facts and patterns in large volumes of data for decision support. This course builds on basic knowledge gained in the introductory data-mining course, and explores how to more effectively mine and manage large volumes of real-world data and to tap into large quantities of data. Working on real world data sets, students will experience all steps of a data-mining and management project, beginning with problem definition and data selection, and continuing through data management, data exploration, data transformation, sampling, portioning, modeling, and assessment.",
    listOfSections: [{
            section: "L1",
            dateTime: "WeFr 01:30PM - 02:50PM",
            room: "G010, CYT Bldg (140)",
            instructor: "WONG, Raymond Chi Wing",
            quota: 65,
            enrol: 64,
            avail: 1,
            wait: 4,
            timeSlot: new Date("2018-01-26T14:00:00Z")
        },
        {
            section: "T1",
            dateTime: "Tu 06:00PM - 06:50PM",
            room: "Rm 4619, Lift 31-32 (126)",
            instructor: "WONG, Raymond Chi Wing",
            quota: 65,
            enrol: 64,
            avail: 1,
            wait: 4,
            timeSlot: new Date("2018-01-26T14:00:00Z")
        },
        {
            section: "L1",
            dateTime: "WeFr 01:30PM - 02:50PM",
            room: "G010, CYT Bldg (140)",
            instructor: "WONG, Raymond Chi Wing",
            quota: 65,
            enrol: 64,
            avail: 1,
            wait: 4,
            timeSlot: new Date("2018-02-01T11:00:00Z")
        }
    ]
})


db.course.insert({
    code: "RMBI4310",
    ctitle: "Advanced Data Mining for Risk Management and Business Intelligence",
    credit: "3",
    prerequisite: [{ code: "COMP 4331" }, { code: "ISOM3360" }],
    colist: [{ code: "COMP4332" }],
    description: "This course will explore some advanced principles and techniques of data mining, with emphasis on applications in risk management and business intelligence. Topics include data mining process for data transformation and integration, data preprocessing, data mining algorithms and evaluation of data mining models and results. Advanced topics include data stream analysis, using data warehouse for decision support, supervised, semi-supervised and unsupervised learning techniques in data mining. We will cover advanced data mining applications in credit risk analysis, scale up methods for mining massive customer data and various novel applications such as data mining applications in social network analysis. Projects are aimed at familiarize the students with the entire data mining process rather than isolated applications.",
    listOfSections: [{
            section: "L1",
            dateTime: "WeFr 01:30PM - 02:50PM",
            room: "G010, CYT Bldg (140)",
            instructor: "WONG, Raymond Chi Wing",
            quota: 55,
            enrol: 43,
            avail: 12,
            wait: 0,
            timeSlot: new Date("2018-01-26T14:00:00Z")
        },
        {
            section: "T1",
            dateTime: "Tu 06:00PM - 06:50PM",
            room: "Rm 4619, Lift 31-32 (126)",
            instructor: "WONG, Raymond Chi Wing",
            quota: 55,
            enrol: 43,
            avail: 12,
            wait: 0,
            timeSlot: new Date("2018-01-26T14:00:00Z")
        }
    ]
})

//db.course.drop()
