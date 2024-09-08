-- Set leader to " " if it isn't already
if vim.g.mapleader ~= " " then vim.g.mapleader = " " end

vim.keymap.set("n", "<leader>e", ":NERDTreeToggle<CR>")
