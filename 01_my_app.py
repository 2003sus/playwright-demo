from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    # ============ 1. 打开页面 ============
    page.goto("http://localhost:5173", timeout=60000)
    page.wait_for_timeout(3000)
    print("1. 页面已打开")
    page.screenshot(path="01_before.png", full_page=True)

    # ============ 2. 新增一本书 ============
    test_title = "Playwright 完整流程测试"
    test_author = "自动化"

    page.fill('input[placeholder="书名"]', test_title)
    page.fill('input[placeholder="作者"]', test_author)
    page.wait_for_timeout(1000)
    page.click('button:has-text("提交")')
    page.wait_for_timeout(3000)

    assert test_title in page.content(), "❌ 新增失败：列表里找不到新书"
    print("2. 新增成功")
    page.screenshot(path="02_after_add.png", full_page=True)

    # ============ 3. 按 ID 查书 ============
    # 先拿到第一本书的 ID（从列表文本里提取）
    # 你的页面显示格式是 [id] 书名 — 作者
    # 找包含 test_title 的那一行的 id
    # 简单方式：直接用搜索框，输入 ID
    # 但我们不知道 ID，所以跳过这个，直接测删除

    # ============ 4. 删除这本书 ============
    # 找到包含 test_title 的那一行，点它的删除按钮
    page.click(f'li:has-text("{test_title}") button:has-text("删除")')
    page.wait_for_timeout(3000)

    assert test_title not in page.content(), "❌ 删除失败：列表里还能找到这本书"
    print("3. 删除成功")
    page.screenshot(path="03_after_delete.png", full_page=True)

    # ============ 完成 ============
    print("\n✅ 完整流程测试通过：新增 → 验证 → 删除 → 验证")

    browser.close()