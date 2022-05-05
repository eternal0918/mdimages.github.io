<template>
	<view>
		<view>
			<global-current-project ref="GlobalCurrentProject"></global-current-project>
			<!-- <uni-section type="line">
				<uni-notice-bar color="#2979FF" background-color="#EAF2FF"
					:text="projtitle" />
			</uni-section> -->
		</view>
		<view class="loop">
			<swiper class="swiper" indicator-dots="true" autoplay="false">
				<swiper-item v-for="(item, index) in loopImages" :key="index">
					<u-image :src="item" height="300rpx"></u-image>
					<!-- <image :src="item" height=></image> -->
				</swiper-item>
			</swiper>
		</view>
		<view @click="toMessagePage">
			<uni-section title="文字滚动" type="line"><uni-notice-bar show-icon scrollable text="设计集团建筑设计师招聘" /></uni-section>
		</view>
		<view class="user-info  center-block comm-wid border  box-shadow ">
			<view class="left">
				<view class="info-block" v-if="userInfo" style="margin-bottom: 10rpx;">
					<text class="font-14">欢迎：</text>
					<text class="main font-16 font-bold">
						<text v-if="userInfo.workType">{{ userInfo.workType + '- ' }}</text>
						{{ userInfo.workerName }}
					</text>
				</view>
				<view class="flex-between flex-align-center" v-if="userInfo">
					<view class="info-block" v-if="['103', '104'].includes(userInfo.teamNum)">
						<text class="font-14">班组：</text>
						<text class="font-16 font-bold">{{ teamName || '' }}</text>
					</view>
					<view class="info-block" v-if="userInfo.teamNum == '102'">
						<text class="font-14">单位：</text>
						<text class="font-16 font-bold">{{ userInfo.roleId || '' }}</text>
					</view>
				</view>
				<view v-if="!userInfo">暂无信息</view>
			</view>

			<view v-if="!isRegister || !isOpenAccount" class="flex-between flex-align-center right">
				<button v-if="!isRegister" class="btn-count" type="primary" size="mini" @click="toRegist()">去身份认证 ></button>
				<button v-if="isRegister && !isOpenAccount" class="btn-count" type="primary" size="mini" @click="toOpenAccount">去开立账户 ></button>
			</view>
		</view>
		<!-- <view class="user-info-work center-block comm-wid border box-shadow mt-20">
			<view class="flex-around mb-20">
				<view class="info-block">
					<text class="font-14">工钱(￥)：</text>
					<text class="font-16 font-bold">1000000</text>
				</view>
				<view class="info-block">
					<text class="font-14">已发工资(￥)：</text>
					<text class="font-16 font-bold">1000000</text>
				</view>
			</view>
			<view class="flex-row flex-around">
				<view class="info-block text-center">
					<view class="font-14">上班时间：</view>
					<view><text class="font-16 ">1000000</text><text class="font-12">个工</text></view>
				</view>
				<view class="info-block text-center">
					<view class="font-14">加班时间：</view>
					<view><text class="font-16 ">1000000</text><text class="font-12">小时</text></view>
				</view>
				<view class="info-block text-center">
					<view class="font-14">按量记：</view>
					<view><text class="font-16 ">1000000</text><text class="font-12">个工程量</text></view>
				</view>
			</view>
		</view> -->
		<view>
			<uni-grid :column="3" :show-border="false" :highlight="false">
				<uni-grid-item v-for="(item, index) in list" :index="index" :key="index">
					<view class="grid-item-box" @click="toPage(item)">
						<view>
							<image :src="item.url" class="image" mode="aspectFill" />
							<text class="text">{{ item.text }}</text>
						</view>
					</view>
				</uni-grid-item>
			</uni-grid>
		</view>
		<view>
			<uni-popup ref="inputDialog">
				<image src="../../static/img/close.png" style="width: 80rpx;height: 80rpx;margin-left: 520rpx;" @click="closePop()"></image>
				<view style="width: 600rpx;height: 660rpx;background: white;border-radius: 20rpx;">
					<image :src="registerImageUrl" style="width: 100%;height: 500rpx;border-top-left-radius: 20rpx;border-top-right-radius: 20rpx;"></image>
					<view class="font-16" style="text-align: center;color: black;">您还未进行身份认证</view>
					<view style="text-align:center;margin-top: 25rpx;"><button type="primary" size="mini" @click="toRegist()">去注册开户</button></view>
				</view>
			</uni-popup>
		</view>
		<uni-popup ref="wxDialog" background-color="#fff">
			<view class="popup-content"><button type="primary" open-type="getPhoneNumber" @getphonenumber="getPhoneNumber">微信一键登录</button></view>
		</uni-popup>
		<update-version :show="updateVersionShow" @cancel="updateVersionShow = false"></update-version>
	</view>
</template>

<script>
import icon from '@/static/tabbar/tool.png';
import { getOpenId, getUser, bindPhone, getBanner } from '@/api/api.js';
import { baseUrl } from '@/utils/request.js';
import UpdateVersion from '@/components/update-version/index.vue';

export default {
	components: {
		UpdateVersion
	},
	data() {
		return {
			updateVersionShow: false,
			projtitle: '',
			loopImages: [],
			btnIcon: icon,
			isRegister: false, // 判断是否实名注册
			isOpenAccount: false, // 判断是否实名开户
			list: [
				// {
				// 	url: '../../static/img/menu-1.png',
				// 	text: '找个零活',
				// 	path1: "/pages/index/lookJobs/index",
				// 	path: ''
				// },
				{
					url: '../../static/img/menu-2.png',
					text: '记工计量',
					path: 'custom',
					checkProject: false
				},
				{
					url: '../../static/img/menu-3.png',
					text: '薪资结算',
					path: 'costom',
					checkProject: true
				},
				{
					url: '../../static/img/menu-4.png',
					text: '进场管理',
					path: 'custom',
					checkProject: true
				},
				{
					url: '../../static/img/menu-5.png',
					text: '退场管理',
					path: '',
					checkProject: true
				},
				{
					url: '../../static/img/menu-6.png',
					text: '维权投诉',
					path: ''
					// path: "/pages/index/complaint/index"
				},
				{
					url: '../../static/img/menu-7.png',
					text: '学个技能',
					path: ''
				}
			],
			userInfo: undefined,
			teamName: ''
		};
	},
	computed: {
		registerImageUrl() {
			return baseUrl + '/profile/pic/4.png';
		}
	},
	onLoad(params) {
		if (params.openid) {
			// 从其它用户分享链接进入会带入分享者的openid  将其存入全局 注册时传给后端
			const app = getApp();
			app.globalData.shareOpenid = params.openid;
		}
		if (!uni.getStorageSync('openid')) {
			uni.login({
				success: async res => {
					console.log('微信login', res);
					const { data } = await getOpenId(res.code);
					uni.setStorageSync('openid', data.openid);
					uni.setStorageSync('session_key', data.session_key);
					this.getQueryUser();
					this.getUser();
					await this.$refs.GlobalCurrentProject.getList();
					const {
						globalData: { currentProject }
					} = getApp();
					this.teamName = currentProject ? currentProject.teamName : '';
				}
			});
		}
		this.getBanner();
	},
	async onShow() {
		if (uni.getStorageSync('openid')) {
			this.getQueryUser();
			this.getUser();
			const {
				globalData: { currentProject }
			} = getApp();
			if (!currentProject) {
				await this.$refs.GlobalCurrentProject.getList();
			} else {
				this.$refs.GlobalCurrentProject.setCurrentProject();
			}
			const {
				globalData: { currentProject: project }
			} = getApp();
			this.teamName = project ? project.teamName : '';
		}
	},
	methods: {
		async getBanner() {
			const { data } = await getBanner();
			this.loopImages = data.map(v => `${baseUrl}${v.path}`);
		},
		// 获取用户信息
		async getUser() {
			try {
				const app = getApp();
				const data = await app.getUser();
				this.userInfo = data;
				if (!data) {
					this.$refs.wxDialog.open('bottom');
				}
			} catch (e) {
				this.$refs.wxDialog.open('bottom');
				//TODO handle the exception
			}
		},
		// 判断用户是否实名注册、是否开户
		async getQueryUser() {
			const { data } = await getUser();
			if (data && data.length) {
				const [{ auth_id, is_account }] = data;
				this.isOpenAccount = !!is_account;
				this.isRegister = !!auth_id;
				if (!this.isRegister) {
					this.openReg();
				}
			} else {
				this.openReg();
			}
		},
		openReg() {
			this.$refs.inputDialog.open();
		},
		toRegist() {
			uni.navigateTo({
				url: '/pages/user/regist'
			});
		},
		toOpenAccount() {
			uni.navigateTo({
				url: '/pages/user/account'
			});
		},
		closePop() {
			this.$refs.inputDialog.close();
		},
		async getPhoneNumber(res) {
			try {
				uni.login({
					success: async res1 => {
						const { data: data1 } = await getOpenId(res1.code);
						const { detail } = res;
						const params = {
							openid: data1.openid,
							sessionkey: data1.session_key,
							iv: detail.iv,
							encryptedData: detail.encryptedData
						};
						const { data } = await bindPhone(params);
						this.$refs.wxDialog.close();
						this.getUser();
						this.getQueryUser();
						if (data.length === 1) {
							const app = getApp();
							app.globalData.currentProject = data[0];
							this.$refs.GlobalCurrentProject.setCurrentProject();
						} else if (data.length > 1) {
							uni.switchTab({
								url: '/pages/changeProj/index'
							});
						}
					}
				});
			} catch (e) {
				this.$refs.wxDialog.close();
				this.openReg();
			}
		},
		toPage({ path, text, checkProject }) {
			console.log('人员权限：', path, text, checkProject);
			if (!this.userInfo) {
				uni.showToast({
					icon: 'error',
					title: '请先注册'
				});
				return;
			}
			if (!path) {
				uni.showToast({
					icon: 'error',
					title: '暂无权限'
				});
				return;
			}
			if (checkProject) {
				const app = getApp();
				if (!app.globalData.currentProject) {
					uni.showToast({
						icon: 'error',
						title: '请先切换项目'
					});
					return;
				}
			}
			if (text == '薪资结算') {
				const app = getApp();
				if (app.globalData.isWorker) {
					uni.navigateTo({
						url: '/pages/wageSettlement/workersWages'
					});
				} else if (app.globalData.isTeam) {
					uni.navigateTo({
						url: '/pages/wageSettlement/teamWages'
					});
				}
			}
			if (text == '进场管理') {
				const app = getApp();
				if (app.globalData.isWorker) {
					uni.navigateTo({
						url: '/pages/entryManage/workerIndex'
					});
				} else if (app.globalData.isTeam) {
					uni.navigateTo({
						url: '/pages/entryManage/teamIndex'
					});
				}
			}
			if (text === '记工计量') {
				// 记工计量判断是否有当前项目
				const app = getApp();
				let pathUrl = '';
				// 根据身份进入不同的页面
				if (app.globalData.isWorker) {
					pathUrl = '/pages/workpointsMeasurement/workpointsMeasurement';
				} else if (app.globalData.isTeam) {
					pathUrl = '/pages/workpointsMeasurement/teamWorkerWorkpointMeasurement';
				}
				uni.navigateTo({
					url: pathUrl
				});
			} else {
				uni.navigateTo({
					url: path
				});
			}
		},
		toMessagePage() {
			uni.navigateTo({
				url: '/pages/message/message'
			});
		}
	}
};
</script>

<style lang="scss" scoped>
page {
	.loop {
		padding: 0;
		width: 100%;
	}
	.border {
		border: 1px solid #ddd;
		border-radius: 20rpx;
	}
	.comm-wid {
		width: 90%;
		padding: 20rpx;
	}

	.user-info {
		display: flex;
		justify-content: space-between;
		.main {
			color: $uni-color-primary;
		}
		.btn-count {
			padding: 0rpx 10rpx;
			font-weight: bold;
			background-color: $uni-color-primary;
			margin: 0;
		}
	}
	.image {
		width: 100rpx;
		height: 100rpx;
	}
	.text {
		font-size: 30rpx;
		margin-top: 5px;
	}
	.grid-item-box {
		flex: 1;
		padding: 20rpx;
		> view {
			height: 100%;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			border: 1px solid #d5d5d5;
			border-radius: 6px;
		}
	}
	.grid-item-box-row {
		flex: 1;
		// position: relative;
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: row;
		align-items: center;
		justify-content: center;
		padding: 15px 0;
	}
}
</style>
