INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Basil', 'Ocimum basilicum', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Thyme', 'Thymus vulgaris', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Rosemary', 'Salvia rosmarinus', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Parsley', 'Petroselinum crispum', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Dill', 'Anethum graveolens', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Oregano', 'Origanum vulgare', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Sage', 'Salvia officinalis', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Lavender', 'Lavandula angustifolia', 'full', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Mint', 'Mentha', 'partial', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Cilantro', 'Coriandrum sativum', 'partial', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Lemon Balm', 'Melissa officinalis', 'partial', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Chives', 'Allium schoenoprasum', 'partial', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Sweet Woodruff', 'Galium odoratum', 'shade', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Valerian', 'Valeriana officinalis', 'shade', 'herb')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Chamomile', 'Matricaria chamomilla', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Calendula', 'Calendula officinalis', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Zinnia', 'Zinnia elegans', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Marigold', 'Tagetes', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Echinacea', 'Echinacea purpurea', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Yarrow', 'Achillea millefolium', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Sunflower', 'Helianthus annuus', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Black-Eyed Susan', 'Rudbeckia hirta', 'full', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Impatiens', 'Impatiens walleriana', 'partial', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Foxglove', 'Digitalis purpurea', 'partial', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Columbine', 'Aquilegia', 'partial', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Astilbe', 'Astilbe', 'partial', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Bleeding Heart', 'Lamprocapnos spectabilis', 'shade', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Hosta', 'Hosta', 'shade', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Lungwort', 'Pulmonaria', 'shade', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Lily of the Valley', 'Convallaria majalis', 'shade', 'flower')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Strawberry', 'Fragaria x ananassa', 'full', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Blueberry', 'Vaccinium corymbosum', 'full', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Raspberry', 'Rubus idaeus', 'full', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Blackberry', 'Rubus allegheniensis', 'full', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Gooseberry', 'Ribes uva-crispa', 'partial', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Elderberry', 'Sambucus nigra', 'partial', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Wild Ginger', 'Asarum canadense', 'shade', 'berry')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Tomato', 'Solanum lycopersicum', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Carrot', 'Daucus carota', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Cucumber', 'Cucumis sativus', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Potato', 'Solanum tuberosum', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Pepper', 'Capsicum annuum', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Zucchini', 'Cucurbita pepo', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Kale', 'Brassica oleracea', 'full', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Lettuce', 'Lactuca sativa', 'partial', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Spinach', 'Spinacia oleracea', 'partial', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Swiss Chard', 'Beta vulgaris', 'partial', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Broccoli', 'Brassica oleracea var. italica', 'partial', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Pea', 'Pisum sativum', 'partial', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Arugula', 'Eruca vesicaria', 'shade', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Sorrel', 'Rumex acetosa', 'shade', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Watercress', 'Nasturtium officinale', 'shade', 'vegetable')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Little Bluestem', 'Schizachyrium scoparium', 'full', 'native grass')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Buffalo Grass', 'Bouteloua dactyloides', 'full', 'native grass')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Switchgrass', 'Panicum virgatum', 'full', 'native grass')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Prairie Dropseed', 'Sporobolus heterolepis', 'full', 'native grass')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Wild Oats', 'Chasmanthium latifolium', 'partial', 'native grass')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('River Oats', 'Chasmanthium latifolium', 'shade', 'native grass')
ON CONFLICT (common_name) DO NOTHING;

INSERT INTO plants (common_name, latin_name, sun, plant_type)
VALUES ('Pennsylvania Sedge', 'Carex pensylvanica', 'shade', 'native grass')
ON CONFLICT (common_name) DO NOTHING;