# API Housing Prices

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Here is my API using FastAPI which provides a simple and powerful interface to estimate the price of your house based on its characteristics.   

## Description  

The objective of this project is mainly GitOps oriented. This project is stored on a Gitlab server that I created with different levels of user management and complete project configuration in order to streamline and secure the creation process. This server has a runner allowing you to carry out numerous automations using pipelines in order to carry out CI/CD of the project.  

![Example](./documentation/image1.jpg)

## Table of Contents

- [Getting Started](#Getting-Started)
- [Launch Application](#Launch-Application)
- [Contributing](#Contributing)
- [License](#License)  

## Getting Started  

You can't use my training model because of Github storage. But if you train your own model you can install and use my repository like this.  

```bash
git clone https://github.com/HaDock404/api-housing-prices.git
cd api-housing-prices
pip install -r ./packages/requirements_api.txt
```  

## Launch Application  

You can't use my training model because of Github storage. But if you train your own model you can install and use my repository like this.  

```bash
uvicorn api:app -—reload
```  

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License  

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.