"""Script para testar scrapers manualmente"""
import asyncio
from datetime import date, timedelta
from app.scrapers.tjsp import TJSPScraper
from app.scrapers.tjrj import TJRJScraper

async def test_scraper(scraper_class, tribunal_name: str):
    """Testa um scraper específico"""
    print(f"\n{'='*60}")
    print(f"Testando {tribunal_name}")
    print(f"{'='*60}")
    
    scraper = scraper_class()
    target_date = date.today() - timedelta(days=1)
    
    print(f"📅 Data alvo: {target_date}")
    print(f"🔍 Iniciando scraping...")
    
    try:
        publications = await scraper.scrape_date(target_date)
        
        print(f"\n✅ Scraping concluído!")
        print(f"📊 Total de publicações encontradas: {len(publications)}")
        
        if publications:
            print(f"\n📄 Exemplo da primeira publicação:")
            first_pub = publications[0]
            print(f"  Tribunal: {first_pub.tribunal}")
            print(f"  Data: {first_pub.publication_date}")
            print(f"  Processo: {first_pub.process_number}")
            print(f"  Tipo: {first_pub.publication_type}")
            print(f"  Partes: {first_pub.parties}")
            print(f"  Conteúdo: {first_pub.content[:100]}...")
        
    except Exception as e:
        print(f"❌ Erro durante scraping: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Testa todos os scrapers"""
    print("🤖 Iniciando teste dos scrapers")
    
    await test_scraper(TJSPScraper, "Tribunal de Justiça de São Paulo")
    await test_scraper(TJRJScraper, "Tribunal de Justiça do Rio de Janeiro")
    
    print(f"\n{'='*60}")
    print("✨ Testes concluídos!")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(main())