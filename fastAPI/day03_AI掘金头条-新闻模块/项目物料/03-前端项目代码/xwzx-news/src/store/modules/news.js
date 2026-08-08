import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [],
    newsDetail: {},
    categories: [],
    currentCategory: 1,
    loading: false,
    refreshing: false,
    finished: false,
    categoriesLoading: false
  }),
  
  actions: {
    // 获取新闻分类
    async getCategories() {
      if (this.categoriesLoading) return;
      
      this.categoriesLoading = true;
      
      try {
        // 调用API获取分类列表
        const response = await axios.get(`${apiConfig.baseURL}/api/news/categories`);
        
        if (response.data && response.data.code === 200) {
          // 设置分类数据
          this.categories = [...response.data.data, { id: 10, name: '更多' }];
          
          // 如果没有设置当前分类，则设置为第一个分类
          if (!this.currentCategory && this.categories.length > 0) {
            this.currentCategory = this.categories[0].id;
          }
        }
      } catch (error) {
        console.error('获取新闻分类失败:', error);
        // 设置默认分类，以防API请求失败
        this.categories = [
          { id: 1, name: '头条' },
          { id: 2, name: '社会' },
          { id: 3, name: '国内' },
          { id: 4, name: '国际' },
          { id: 5, name: '娱乐' },
          { id: 6, name: '体育' },
          { id: 7, name: '科技' }
        ];
      } finally {
        this.categoriesLoading = false;
      }
    },
    
    // 获取新闻列表
    async getNewsList(isRefresh = false) {
      if (isRefresh) {
        this.refreshing = true
        this.newsList = []
        this.finished = false
      }
      
      this.loading = true
      
      try {
        // 使用API请求获取新闻列表
        const params = {
          categoryId: this.currentCategory,
          page: isRefresh ? 1 : Math.ceil(this.newsList.length / 10) + 1,
          pageSize: 10
        }
        
        // 在开发环境中，直接使用模拟数据
        // console.log('使用模拟新闻列表数据');
        
        // 生成模拟数据
        // const mockData = Array.from({ length: 10 }, (_, index) => ({
        //   id: isRefresh ? index + 1 : this.newsList.length + index + 1,
        //   title: `${this.getCategoryName(this.currentCategory)}新闻${isRefresh ? index + 1 : this.newsList.length + index + 1}`,
        //   description: `这是一条关于${this.getCategoryName(this.currentCategory)}的新闻简介，包含了新闻的主要内容和亮点。`,
        //   image: `https://picsum.photos/id/${Math.floor(Math.random() * 100)}/200/200`,
        //   author: '新闻资讯',
        //   publishTime: new Date().toLocaleString(),
        //   categoryId: this.currentCategory,
        //   views: Math.floor(Math.random() * 10000)
        // }))
        
        // this.newsList = isRefresh ? mockData : [...this.newsList, ...mockData]
        
        // 模拟数据加载完成的逻辑
        // if (this.newsList.length >= 30) {
        //   this.finished = true
        // }
        
 
        // 实际项目中连接后端API的代码，暂时注释掉
        const response = await axios.get(`${apiConfig.baseURL}/api/news/list`, { params });
        
        if (response.data && response.data.code === 200) {
          const newsData = response.data.data.list;
          
          // 更新新闻列表
          this.newsList = isRefresh ? newsData : [...this.newsList, ...newsData];
          
          // 判断是否加载完成
          if (newsData.length < params.pageSize) {
            this.finished = true;
          }
        }

      } catch (error) {
        console.error('获取新闻列表失败:', error)
      } finally {
        this.loading = false
        this.refreshing = false
      }
    },
    
    // 获取新闻详情
    async getNewsDetail(id) {
      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/detail?id=${id}`);
        
        if (response.data && response.data.code === 200) {
          this.newsDetail = response.data.data;
        } else {
          console.error('获取新闻详情失败: 接口返回错误');
        }
      } catch (error) {
        console.error('获取新闻详情失败:', error);
      }
    },
    
    // 切换新闻分类
    changeCategory(categoryId) {
      if (this.currentCategory !== categoryId) {
        this.currentCategory = categoryId
        this.newsList = []
        this.finished = false
        this.getNewsList(true)
      }
    },
    
    // 获取分类名称
    getCategoryName(categoryId) {
      const category = this.categories.find(item => item.id === categoryId)
      return category ? category.name : '未知'
    }
  }
})