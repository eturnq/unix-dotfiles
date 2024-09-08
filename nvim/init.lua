-- bootstrap lazy and all plugins 
local lazypath = vim.fn.stdpath "data" .. "/lazy/lazy.nvim"

if not vim.uv.fs_stat(lazypath) then
  local repo = "https://github.com/folke/lazy.nvim.git"
  vim.fn.system { "git", "clone", "--filter=blob:none", repo, "--branch=stable", lazypath }
end

vim.opt.rtp:prepend(lazypath)

-- load plugins 
local lazy_config = require "configs.lazy"
vim.g.mapleader = " " -- Leader must be set before Lazy can be loaded
require("lazy").setup({
  { import = "plugins" },
}, lazy_config )

-- load theme
-- dofile(vim.g.base46_cache .. "defaults")
-- dofile(vim.g.base46_cache .. "statusline")

-- require "options"
-- require "autocmds"
--
vim.schedule(function()
  require "after"
end)
