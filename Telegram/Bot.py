import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


class TelegramBot:
    def __init__(self, ac_controller, bot_token):
        self.ac_controller = ac_controller
        self.bot_token = bot_token
        self.application = None
        self.logger = logging.getLogger('TelegramBot')
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        self.logger.info(f"Start command received from user {update.effective_user.id if update.effective_user else 'Unknown'}")
        if update.message:
            await update.message.reply_text(
                "🏠 AC Controller Bot\n\n"
                "Available commands:\n"
                "/status - Check AC status\n"
                "/toggle - Toggle AC manually\n"
                "/auto_start [minutes] - Start auto-toggle (default 10 min)\n"
                "/auto_stop - Stop auto-toggle\n"
                "/help - Show this help message"
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await self.start_command(update, context)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        self.logger.info(f"Status command received from user {update.effective_user.id if update.effective_user else 'Unknown'}")
        status = self.ac_controller.get_status()
        ac_status = "🟢 ON" if status["ac_on"] else "🔴 OFF"
        auto_status = "🔄 ACTIVE" if status["auto_toggle_active"] else "⏹️ STOPPED"
        
        message = (
            f"🏠 AC Status: {ac_status}\n"
            f"🤖 Auto-toggle: {auto_status}\n"
            f"⏱️ Interval: {status['auto_toggle_interval']} seconds"
        )
        self.logger.info(f"Status response: AC={status['ac_on']}, Auto={status['auto_toggle_active']}")
        if update.message:
            await update.message.reply_text(message)
    
    async def toggle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /toggle command"""
        self.logger.info(f"Toggle command received from user {update.effective_user.id if update.effective_user else 'Unknown'}")
        if self.ac_controller.toggle_ac():
            status = "🟢 ON" if self.ac_controller.ac_on else "🔴 OFF"
            self.logger.info(f"AC toggle successful. New state: {status}")
            if update.message:
                await update.message.reply_text(f"✅ AC toggled successfully!\nAC is now: {status}")
        else:
            self.logger.error("AC toggle failed")
            if update.message:
                await update.message.reply_text("❌ Failed to toggle AC")
    
    async def auto_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /auto_start command"""
        self.logger.info(f"Auto-start command received from user {update.effective_user.id if update.effective_user else 'Unknown'}")
        interval_minutes = 10  # default
        
        if context.args:
            try:
                interval_minutes = int(context.args[0])
                if interval_minutes < 1:
                    self.logger.warning(f"Invalid interval requested: {interval_minutes} minutes")
                    if update.message:
                        await update.message.reply_text("❌ Interval must be at least 1 minute")
                    return
            except ValueError:
                self.logger.warning(f"Invalid interval format: {context.args[0]}")
                if update.message:
                    await update.message.reply_text("❌ Please provide a valid number of minutes")
                return
        
        interval_seconds = interval_minutes * 60
        if self.ac_controller.start_auto_toggle(interval_seconds):
            self.logger.info(f"Auto-toggle started with {interval_minutes} minute interval")
            if update.message:
                await update.message.reply_text(
                    f"🔄 Auto-toggle started!\n"
                    f"⏱️ Interval: {interval_minutes} minutes"
                )
        else:
            self.logger.warning("Auto-toggle start failed - already active")
            if update.message:
                await update.message.reply_text("❌ Auto-toggle is already active")
    
    async def auto_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /auto_stop command"""
        self.logger.info(f"Auto-stop command received from user {update.effective_user.id if update.effective_user else 'Unknown'}")
        if self.ac_controller.stop_auto_toggle():
            self.logger.info("Auto-toggle stopped successfully")
            if update.message:
                await update.message.reply_text("⏹️ Auto-toggle stopped")
        else:
            self.logger.warning("Auto-toggle stop failed - not active")
            if update.message:
                await update.message.reply_text("❌ Auto-toggle is not active")
    
    def run(self):
        """Start the bot"""
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("toggle", self.toggle_command))
        self.application.add_handler(CommandHandler("auto_start", self.auto_start_command))
        self.application.add_handler(CommandHandler("auto_stop", self.auto_stop_command))
        
        self.logger.info("Starting Telegram bot...")
        print("Starting Telegram bot...")  # Keep this as print for user confirmation
        self.application.run_polling()
