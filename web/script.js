// JavaScript for Freemasonry Twitter Scraper Interface

class TwitterScraperApp {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.currentData = {
            tweets: [],
            users: [],
            accounts: []
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadStoredData();
        this.updateUI();
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.closest('.tab-btn').dataset.tab);
            });
        });

        // Forms
        document.getElementById('search-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSearch();
        });

        document.getElementById('account-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddAccount();
        });

        // Quick actions
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.closest('.action-btn').onclick;
                if (action) action();
            });
        });
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        // Update specific tab data
        if (tabName === 'accounts') {
            this.loadAccounts();
        } else if (tabName === 'results') {
            this.displayResults();
        } else if (tabName === 'ai-config') {
            this.loadBusinessConfig();
            this.checkClaudeStatus();
        }
    }

    async handleSearch() {
        const query = document.getElementById('search-query').value;
        const limit = parseInt(document.getElementById('search-limit').value);
        const searchType = document.getElementById('search-type').value;

        if (!query.trim()) {
            this.showNotification('Please enter a search query', 'warning');
            return;
        }

        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiUrl}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    limit: limit,
                    product: searchType
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.success) {
                this.currentData.tweets = [...this.currentData.tweets, ...data.tweets];
                this.saveData();
                this.updateStats();
                this.addActivity(`Searched for "${query}" - found ${data.tweets.length} tweets`);
                this.showNotification(`Found ${data.tweets.length} tweets!`, 'success');
                this.switchTab('results');
            } else {
                throw new Error(data.error || 'Search failed');
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showNotification(`Search failed: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async handleAddAccount() {
        const username = document.getElementById('account-username').value;
        const password = document.getElementById('account-password').value;
        const email = document.getElementById('account-email').value;
        const emailPassword = document.getElementById('account-email-password').value;
        const cookies = document.getElementById('account-cookies').value;

        if (!username || !password || !email) {
            this.showNotification('Please fill in all required fields', 'warning');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiUrl}/accounts/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    email: email,
                    email_password: emailPassword,
                    cookies: cookies
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.loadAccounts();
                this.clearForm('account-form');
                this.addActivity(`Added account: ${username}`);
                this.showNotification('Account added successfully!', 'success');
            } else {
                throw new Error(data.error || 'Failed to add account');
            }
        } catch (error) {
            console.error('Add account error:', error);
            this.showNotification(`Failed to add account: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async getUserInfo() {
        const username = document.getElementById('username').value;
        if (!username.trim()) {
            this.showNotification('Please enter a username', 'warning');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiUrl}/user/${username}`);
            const data = await response.json();
            
            if (data.success) {
                this.currentData.users.push(data.user);
                this.saveData();
                this.addActivity(`Retrieved user info for @${username}`);
                this.showNotification(`User info retrieved for @${username}`, 'success');
                this.displayUserInfo(data.user);
            } else {
                throw new Error(data.error || 'Failed to get user info');
            }
        } catch (error) {
            console.error('Get user error:', error);
            this.showNotification(`Failed to get user info: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async getUserTweets() {
        const username = document.getElementById('username').value;
        const limit = 10; // Default limit

        if (!username.trim()) {
            this.showNotification('Please enter a username', 'warning');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiUrl}/user/${username}/tweets?limit=${limit}`);
            const data = await response.json();
            
            if (data.success) {
                this.currentData.tweets = [...this.currentData.tweets, ...data.tweets];
                this.saveData();
                this.updateStats();
                this.addActivity(`Retrieved ${data.tweets.length} tweets from @${username}`);
                this.showNotification(`Retrieved ${data.tweets.length} tweets from @${username}`, 'success');
                this.switchTab('results');
            } else {
                throw new Error(data.error || 'Failed to get user tweets');
            }
        } catch (error) {
            console.error('Get user tweets error:', error);
            this.showNotification(`Failed to get user tweets: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async loadAccounts() {
        try {
            const response = await fetch(`${this.apiUrl}/accounts`);
            const data = await response.json();
            
            if (data.success) {
                this.currentData.accounts = data.accounts;
                this.displayAccounts();
                this.updateAccountCount();
            }
        } catch (error) {
            console.error('Load accounts error:', error);
            this.showNotification('Failed to load accounts', 'error');
        }
    }

    displayAccounts() {
        const accountsList = document.getElementById('accounts-list');
        
        if (this.currentData.accounts.length === 0) {
            accountsList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-users"></i>
                    <p>No accounts connected yet.</p>
                    <p>Add your Twitter accounts above to get started.</p>
                </div>
            `;
            return;
        }

        accountsList.innerHTML = this.currentData.accounts.map(account => `
            <div class="account-item">
                <div class="account-info">
                    <i class="fas fa-user"></i>
                    <div>
                        <div class="account-username">@${account.username}</div>
                        <div class="account-email">${account.email}</div>
                    </div>
                </div>
                <div class="account-status ${account.active ? 'active' : 'inactive'}">
                    ${account.active ? 'Active' : 'Inactive'}
                </div>
            </div>
        `).join('');
    }

    displayResults() {
        const resultsList = document.getElementById('results-list');
        
        if (this.currentData.tweets.length === 0) {
            resultsList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <p>No search results yet.</p>
                    <p>Use the Search tab to start scraping tweets.</p>
                </div>
            `;
            return;
        }

        resultsList.innerHTML = this.currentData.tweets.map((tweet, index) => `
            <div class="result-item" data-tweet-index="${index}">
                <div class="result-header">
                    <span class="result-user">@${tweet.username || 'unknown'}</span>
                    <span class="result-date">${this.formatDate(tweet.date)}</span>
                    <div class="result-actions">
                        <button class="generate-reply-btn" onclick="generateReply(${index})" title="Generate AI reply">
                            <i class="fas fa-robot"></i>
                        </button>
                        ${tweet.url ? `<button class="open-tweet-btn" onclick="openTweetInNewWindow('${tweet.url}')" title="Open tweet in new window">
                            <i class="fas fa-external-link-alt"></i>
                        </button>` : ''}
                    </div>
                </div>
                <div class="result-content">${this.truncateText(tweet.content, 200)}</div>
                <div class="result-stats">
                    <span><i class="fas fa-heart"></i> ${tweet.likes || 0}</span>
                    <span><i class="fas fa-retweet"></i> ${tweet.retweets || 0}</span>
                    <span><i class="fas fa-comment"></i> ${tweet.replies || 0}</span>
                    ${tweet.views ? `<span><i class="fas fa-eye"></i> ${tweet.views}</span>` : ''}
                </div>
                <div class="generated-reply" id="reply-${index}" style="display: none;">
                    <div class="reply-header">
                        <h4><i class="fas fa-robot"></i> AI Generated Reply</h4>
                        <div class="reply-actions">
                            <button class="copy-reply-btn" onclick="copyReply(${index})" title="Copy to clipboard">
                                <i class="fas fa-copy"></i>
                            </button>
                            <button class="edit-reply-btn" onclick="editReply(${index})" title="Edit reply">
                                <i class="fas fa-edit"></i>
                            </button>
                        </div>
                    </div>
                    <div class="reply-content" id="reply-content-${index}"></div>
                    <div class="reply-stats" id="reply-stats-${index}"></div>
                </div>
            </div>
        `).join('');
    }

    displayUserInfo(user) {
        // Create a modal or dedicated section to show user info
        const modal = document.createElement('div');
        modal.className = 'user-info-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>User Information</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="user-info">
                    <div class="user-avatar">
                        <img src="${user.profile_image || '/api/placeholder/100/100'}" alt="Profile">
                    </div>
                    <div class="user-details">
                        <h4>@${user.username}</h4>
                        <p class="display-name">${user.displayname || user.username}</p>
                        <p class="bio">${user.bio || 'No bio available'}</p>
                        <div class="user-stats">
                            <span><strong>${user.followers || 0}</strong> Followers</span>
                            <span><strong>${user.following || 0}</strong> Following</span>
                            <span><strong>${user.tweets || 0}</strong> Tweets</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal functionality
        modal.querySelector('.close-modal').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }

    updateStats() {
        document.getElementById('total-tweets').textContent = this.currentData.tweets.length;
        document.getElementById('total-users').textContent = this.currentData.users.length;
        document.getElementById('last-search').textContent = new Date().toLocaleTimeString();
    }

    updateAccountCount() {
        const activeAccounts = this.currentData.accounts.filter(acc => acc.active).length;
        document.getElementById('active-accounts').textContent = activeAccounts;
        document.getElementById('account-count').textContent = `${this.currentData.accounts.length} accounts connected`;
    }

    addActivity(message) {
        const activityList = document.getElementById('activity-list');
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `
            <i class="fas fa-info-circle"></i>
            <span>${message}</span>
            <span class="time">${new Date().toLocaleTimeString()}</span>
        `;
        
        activityList.insertBefore(activityItem, activityList.firstChild);
        
        // Keep only last 10 activities
        while (activityList.children.length > 10) {
            activityList.removeChild(activityList.lastChild);
        }
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        overlay.style.display = show ? 'flex' : 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'warning' ? 'exclamation' : 'info'}-circle"></i>
            <span>${message}</span>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 5000);
    }

    clearForm(formId) {
        const form = document.getElementById(formId);
        form.reset();
    }

    exportResults() {
        if (this.currentData.tweets.length === 0) {
            this.showNotification('No data to export', 'warning');
            return;
        }

        const dataStr = JSON.stringify(this.currentData, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(dataBlob);
        link.download = `twitter_scraper_data_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        this.addActivity('Data exported to JSON file');
        this.showNotification('Data exported successfully!', 'success');
    }

    clearData() {
        if (confirm('Are you sure you want to clear all scraped data? This cannot be undone.')) {
            this.currentData.tweets = [];
            this.currentData.users = [];
            this.saveData();
            this.updateStats();
            this.displayResults();
            this.addActivity('All scraped data cleared');
            this.showNotification('Data cleared successfully', 'success');
        }
    }

    clearResults() {
        this.clearData();
    }

    refreshAccounts() {
        this.loadAccounts();
        this.addActivity('Account list refreshed');
    }

    saveData() {
        localStorage.setItem('twitter_scraper_data', JSON.stringify(this.currentData));
    }

    loadStoredData() {
        const stored = localStorage.getItem('twitter_scraper_data');
        if (stored) {
            this.currentData = JSON.parse(stored);
        }
    }

    updateUI() {
        this.updateStats();
        this.updateAccountCount();
        this.displayResults();
    }

    formatDate(dateString) {
        if (!dateString) return 'Unknown';
        const date = new Date(dateString);
        return date.toLocaleString();
    }

    truncateText(text, maxLength) {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    async generateReply(tweetIndex) {
        const tweet = this.currentData.tweets[tweetIndex];
        if (!tweet) {
            this.showNotification('Tweet not found', 'error');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiUrl}/generate-reply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tweet_content: tweet.content,
                    tweet_author: tweet.username
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.displayGeneratedReply(tweetIndex, data.reply, data.character_count);
                this.addActivity(`Generated AI reply for tweet by @${tweet.username}`);
                this.showNotification('AI reply generated successfully!', 'success');
            } else {
                throw new Error(data.error || 'Failed to generate reply');
            }
        } catch (error) {
            console.error('Generate reply error:', error);
            this.showNotification(`Failed to generate reply: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayGeneratedReply(tweetIndex, reply, characterCount) {
        const replyElement = document.getElementById(`reply-${tweetIndex}`);
        const replyContent = document.getElementById(`reply-content-${tweetIndex}`);
        const replyStats = document.getElementById(`reply-stats-${tweetIndex}`);
        
        if (replyElement && replyContent && replyStats) {
            replyContent.innerHTML = `<p class="reply-text">${reply}</p>`;
            replyStats.innerHTML = `<span class="char-count ${characterCount > 280 ? 'over-limit' : ''}">${characterCount}/280 characters</span>`;
            replyElement.style.display = 'block';
            
            // Store the reply in the tweet data
            this.currentData.tweets[tweetIndex].generatedReply = reply;
            this.saveData();
        }
    }

    copyReply(tweetIndex) {
        const tweet = this.currentData.tweets[tweetIndex];
        if (tweet && tweet.generatedReply) {
            navigator.clipboard.writeText(tweet.generatedReply).then(() => {
                this.showNotification('Reply copied to clipboard!', 'success');
                this.addActivity(`Copied AI reply for tweet by @${tweet.username}`);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                this.showNotification('Failed to copy reply', 'error');
            });
        }
    }

    editReply(tweetIndex) {
        const tweet = this.currentData.tweets[tweetIndex];
        const replyContent = document.getElementById(`reply-content-${tweetIndex}`);
        
        if (tweet && tweet.generatedReply && replyContent) {
            const currentReply = tweet.generatedReply;
            
            replyContent.innerHTML = `
                <div class="reply-editor">
                    <textarea class="reply-textarea" maxlength="280">${currentReply}</textarea>
                    <div class="editor-actions">
                        <button class="save-reply-btn" onclick="saveEditedReply(${tweetIndex})">
                            <i class="fas fa-save"></i> Save
                        </button>
                        <button class="cancel-edit-btn" onclick="cancelEdit(${tweetIndex})">
                            <i class="fas fa-times"></i> Cancel
                        </button>
                    </div>
                    <div class="char-counter">
                        <span id="edit-char-count-${tweetIndex}">${currentReply.length}/280</span>
                    </div>
                </div>
            `;
            
            // Add character counter for textarea
            const textarea = replyContent.querySelector('.reply-textarea');
            const charCounter = document.getElementById(`edit-char-count-${tweetIndex}`);
            
            textarea.addEventListener('input', () => {
                const count = textarea.value.length;
                charCounter.textContent = `${count}/280`;
                charCounter.className = count > 280 ? 'over-limit' : '';
            });
        }
    }

    saveEditedReply(tweetIndex) {
        const replyContent = document.getElementById(`reply-content-${tweetIndex}`);
        const textarea = replyContent.querySelector('.reply-textarea');
        
        if (textarea) {
            const newReply = textarea.value.trim();
            if (newReply) {
                this.currentData.tweets[tweetIndex].generatedReply = newReply;
                this.saveData();
                this.displayGeneratedReply(tweetIndex, newReply, newReply.length);
                this.addActivity(`Edited AI reply for tweet`);
                this.showNotification('Reply updated successfully!', 'success');
            }
        }
    }

    cancelEdit(tweetIndex) {
        const tweet = this.currentData.tweets[tweetIndex];
        if (tweet && tweet.generatedReply) {
            this.displayGeneratedReply(tweetIndex, tweet.generatedReply, tweet.generatedReply.length);
        }
    }

    async loadBusinessConfig() {
        try {
            const response = await fetch(`${this.apiUrl}/business-context`);
            const data = await response.json();
            
            if (data.success) {
                this.populateConfigForm(data.context);
            } else {
                this.showNotification('Failed to load business configuration', 'error');
            }
        } catch (error) {
            console.error('Load business config error:', error);
            this.showNotification('Failed to load business configuration', 'error');
        }
    }

    populateConfigForm(context) {
        document.getElementById('company-name').value = context.company_name || '';
        document.getElementById('industry').value = context.industry || '';
        document.getElementById('tone').value = context.tone || 'professional';
        document.getElementById('target-audience').value = context.target_audience || '';
        document.getElementById('personality').value = context.personality || '';
        document.getElementById('key-services').value = context.key_services ? context.key_services.join(', ') : '';
        document.getElementById('brand-values').value = context.brand_values ? context.brand_values.join(', ') : '';
        document.getElementById('reply-guidelines').value = context.reply_guidelines ? context.reply_guidelines.join('\n') : '';
        document.getElementById('avoid-topics').value = context.avoid_topics ? context.avoid_topics.join(', ') : '';
    }

    async saveBusinessConfig() {
        const context = {
            company_name: document.getElementById('company-name').value,
            industry: document.getElementById('industry').value,
            tone: document.getElementById('tone').value,
            target_audience: document.getElementById('target-audience').value,
            personality: document.getElementById('personality').value,
            key_services: document.getElementById('key-services').value.split(',').map(s => s.trim()).filter(s => s),
            brand_values: document.getElementById('brand-values').value.split(',').map(s => s.trim()).filter(s => s),
            reply_guidelines: document.getElementById('reply-guidelines').value.split('\n').map(s => s.trim()).filter(s => s),
            avoid_topics: document.getElementById('avoid-topics').value.split(',').map(s => s.trim()).filter(s => s)
        };

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiUrl}/business-context`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ context })
            });

            const data = await response.json();
            
            if (data.success) {
                this.addActivity('Updated AI business configuration');
                this.showNotification('Business configuration saved successfully!', 'success');
            } else {
                throw new Error(data.error || 'Failed to save configuration');
            }
        } catch (error) {
            console.error('Save business config error:', error);
            this.showNotification(`Failed to save configuration: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async checkClaudeStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            const data = await response.json();
            
            const statusElement = document.getElementById('claude-status');
            if (data.claude_available) {
                statusElement.innerHTML = '<span style="color: #28a745;">✓ Connected</span>';
            } else {
                statusElement.innerHTML = '<span style="color: #dc3545;">✗ Not Available</span>';
            }
            
            // Check wandb status if available
            if (data.wandb_available && data.wandb_initialized) {
                this.loadWandbInfo();
            }
        } catch (error) {
            const statusElement = document.getElementById('claude-status');
            statusElement.innerHTML = '<span style="color: #dc3545;">✗ Error</span>';
        }
    }

    async loadWandbInfo() {
        try {
            const response = await fetch(`${this.apiUrl}/wandb/metrics`);
            const data = await response.json();
            
            if (data.success && data.metrics) {
                this.displayWandbInfo(data.metrics);
            }
        } catch (error) {
            console.error('Failed to load wandb info:', error);
        }
    }

    displayWandbInfo(metrics) {
        const configStatus = document.getElementById('config-status');
        if (configStatus && metrics.url) {
            const wandbInfo = document.createElement('div');
            wandbInfo.className = 'wandb-info';
            wandbInfo.innerHTML = `
                <p><strong>Weights & Biases:</strong> <span style="color: #28a745;">✓ Connected</span></p>
                <p><strong>Project:</strong> ${metrics.project || 'N/A'}</p>
                <p><strong>Run:</strong> ${metrics.run_name || 'N/A'}</p>
                <p><a href="${metrics.url}" target="_blank" style="color: var(--gold-accent);">
                    <i class="fas fa-external-link-alt"></i> View Dashboard
                </a></p>
            `;
            configStatus.appendChild(wandbInfo);
        }
    }
}

// Global functions for inline event handlers
function switchTab(tabName) {
    app.switchTab(tabName);
}

function getUserInfo() {
    app.getUserInfo();
}

function getUserTweets() {
    app.getUserTweets();
}

function exportResults() {
    app.exportResults();
}

function clearData() {
    app.clearData();
}

function refreshAccounts() {
    app.refreshAccounts();
}

function clearResults() {
    app.clearResults();
}

function openTweetInNewWindow(tweetUrl) {
    if (tweetUrl) {
        window.open(tweetUrl, '_blank', 'noopener,noreferrer');
        app.addActivity(`Opened tweet in new window: ${tweetUrl}`);
    }
}

function generateReply(tweetIndex) {
    app.generateReply(tweetIndex);
}

function copyReply(tweetIndex) {
    app.copyReply(tweetIndex);
}

function editReply(tweetIndex) {
    app.editReply(tweetIndex);
}

function saveEditedReply(tweetIndex) {
    app.saveEditedReply(tweetIndex);
}

function cancelEdit(tweetIndex) {
    app.cancelEdit(tweetIndex);
}

function loadBusinessConfig() {
    app.loadBusinessConfig();
}

function saveBusinessConfig() {
    app.saveBusinessConfig();
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TwitterScraperApp();
});

// Add notification styles dynamically
const notificationStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 300px;
        animation: slideIn 0.3s ease;
    }
    
    .notification-success { background: #28a745; }
    .notification-warning { background: #ffc107; color: #000; }
    .notification-error { background: #dc3545; }
    .notification-info { background: #17a2b8; }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .user-info-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1002;
    }
    
    .modal-content {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 24px;
        max-width: 500px;
        width: 90%;
        border: 1px solid var(--border-color);
    }
    
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .close-modal {
        background: none;
        border: none;
        color: var(--text-primary);
        font-size: 24px;
        cursor: pointer;
    }
    
    .user-info {
        display: flex;
        gap: 20px;
        align-items: start;
    }
    
    .user-avatar img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 2px solid var(--gold-accent);
    }
    
    .user-details h4 {
        color: var(--gold-accent);
        margin-bottom: 5px;
    }
    
    .user-stats {
        display: flex;
        gap: 15px;
        margin-top: 15px;
        font-size: 0.9rem;
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    .result-actions {
        display: flex;
        gap: 8px;
    }
    
    .open-tweet-btn {
        background: var(--gold-accent);
        border: none;
        border-radius: 6px;
        color: white;
        padding: 6px 10px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .open-tweet-btn:hover {
        background: #d4a843;
        transform: translateY(-1px);
    }
    
    .open-tweet-btn:active {
        transform: translateY(0);
    }
    
    .generate-reply-btn {
        background: #6c63ff;
        border: none;
        border-radius: 6px;
        color: white;
        padding: 6px 10px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 5px;
        margin-right: 8px;
    }
    
    .generate-reply-btn:hover {
        background: #5a54d6;
        transform: translateY(-1px);
    }
    
    .generate-reply-btn:active {
        transform: translateY(0);
    }
    
    .generated-reply {
        margin-top: 15px;
        padding: 15px;
        background: var(--input-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        border-left: 4px solid #6c63ff;
    }
    
    .reply-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .reply-header h4 {
        color: #6c63ff;
        margin: 0;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .reply-actions {
        display: flex;
        gap: 8px;
    }
    
    .copy-reply-btn, .edit-reply-btn {
        background: var(--gold-accent);
        border: none;
        border-radius: 4px;
        color: white;
        padding: 4px 8px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .copy-reply-btn:hover, .edit-reply-btn:hover {
        background: #d4a843;
    }
    
    .reply-text {
        margin: 10px 0;
        line-height: 1.5;
        color: var(--text-primary);
    }
    
    .reply-stats {
        margin-top: 10px;
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    .char-count {
        color: #28a745;
    }
    
    .char-count.over-limit {
        color: #dc3545;
        font-weight: bold;
    }
    
    .reply-editor {
        margin: 10px 0;
    }
    
    .reply-textarea {
        width: 100%;
        min-height: 80px;
        padding: 10px;
        border: 1px solid var(--border-color);
        border-radius: 6px;
        background: var(--input-bg);
        color: var(--text-primary);
        font-family: inherit;
        font-size: 0.9rem;
        resize: vertical;
        box-sizing: border-box;
    }
    
    .reply-textarea:focus {
        outline: none;
        border-color: var(--gold-accent);
    }
    
    .editor-actions {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    .save-reply-btn, .cancel-edit-btn {
        padding: 6px 12px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    
    .save-reply-btn {
        background: #28a745;
        color: white;
    }
    
    .save-reply-btn:hover {
        background: #218838;
    }
    
    .cancel-edit-btn {
        background: #6c757d;
        color: white;
    }
    
    .cancel-edit-btn:hover {
        background: #5a6268;
    }
    
    .char-counter {
        margin-top: 8px;
        text-align: right;
        font-size: 0.8rem;
        color: var(--text-secondary);
    }
    
    .char-counter .over-limit {
        color: #dc3545;
        font-weight: bold;
    }
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);